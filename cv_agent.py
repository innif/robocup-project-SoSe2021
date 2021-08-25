# Finn
import base64

import cv2
import numpy as np

from robolib.pynaoqi_wrapper import vision_definitions
from robolib import NaoqiClientAgent


hsv_vals_ball = (18, 158, 152)
hsv_vals_goal_y = (38, 141, 158)
hsv_vals_goal_b = (110, 188, 179)

debug = True


class CVAgent:
    def __init__(self, server_uri):
        self._agent = NaoqiClientAgent(server_uri)
        self.goal_center = (0, 0)  # Center of Goal in Pixels
        self.goal_size = (0, 0)  # width, height

        self.goal_b = None
        self.goal_y = None
        self.ball = None

        resolution = vision_definitions.kVGA
        color_space = vision_definitions.kRGBColorSpace
        self._agent.subscribe_to_cam(resolution, color_space)
        self.img_hsv = None
        self.img = None

    def update(self, target="blue") -> None:
        self.img = self.get_image()
        self.img_hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        self.ball, cnt_ball = self.__find_ball(hsv_vals_ball)
        self.goal_b, cnt_goal_b = self.__find_goal(hsv_vals_goal_b)
        self.goal_y, cnt_goal_y = self.__find_goal(hsv_vals_goal_y)

        if target == "blue":
            goal = self.goal_b
        elif target == "yellow":
            goal = self.goal_y
        else:
            goal = None

        if goal is not None:
            self.goal_center, self.goal_size = goal
            self.goal_center = self.__to_centered_coordinates(self.goal_center)
        else:
            self.goal_size = None
            self.goal_center = None

        if debug:
            img_debug = self.img.copy()
            self.__draw_objects(img_debug)
            cnt_list = []
            for cnt in [cnt_goal_b, cnt_goal_y, cnt_ball]:
                if cnt is not None:
                    cnt_list.append(cnt)
            cv2.drawContours(img_debug, cnt_list, -1, (0, 0, 255), 2)
            cv2.imshow('with Blobs', img_debug)
            cv2.waitKey(1)

    def get_image(self):
        nao_image = self._agent.get_image()
        img_decoded = base64.b64decode(nao_image[6])
        img = (np.reshape(np.frombuffer(img_decoded, dtype='%iuint8' % nao_image[2]),
                          (nao_image[1], nao_image[0], nao_image[2])))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img

    def __draw_objects(self, img):
        if self.ball:
            (x, y), radius = self.ball
            cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 0), 2)
        for goal in [self.goal_y, self.goal_b]:
            if goal:
                (x, y), (w, h) = goal
                p1 = (int(x - w/2), int(y - h/2))
                p2 = (int(x + w/2), int(y + h/2))
                cv2.rectangle(img, p1, p2, (0, 255, 0), 2)

    def __search_for_color(self, color):
        img_better = self.__calc_similarity_picture(color)
        img_thresh = self.__calc_threshold(img_better)
        return self.__find_contour_in_mask(img_thresh)

    def __find_goal(self, color):
        contour = self.__search_for_color(color)
        if contour is None:
            return None, None
        return self.__get_surrounding_rect(contour), contour

    def __find_ball(self, color):
        contour = self.__search_for_color(color)
        if contour is None:
            return None, None
        (x, y), radius = cv2.minEnclosingCircle(contour)
        return ((x, y), radius), contour

    def __calc_similarity_picture(self, color):
        wanted_h, wanted_s, wanted_v = color

        img_h = self.img_hsv[:, :, 0].astype(np.int32)
        img_s = self.img_hsv[:, :, 1].astype(np.int32)
        img_v = self.img_hsv[:, :, 2].astype(np.int32)

        # improve H
        img_h -= int(wanted_h)
        img_h = np.where(img_h < -90, img_h + 180, img_h)
        img_h = np.where(img_h > 90, img_h - 180, img_h)
        img_h = np.where(img_h < 0, -img_h, img_h)
        img_h = np.where(img_h > 255, 255, img_h)
        img_h = img_h.astype(np.uint8)

        # improve S
        img_s = wanted_s - img_s
        img_s = np.where(img_s < 0, 0, img_s)
        img_s = img_s / 10
        img_s *= img_s
        img_s = np.where(img_s > 255, 255, img_s)
        img_s = img_s.astype(np.uint8)

        # improve V
        img_v = wanted_v - img_v
        img_v = np.where(img_v < 0, 0, img_v)
        img_v = img_v / 12
        img_v *= 2
        img_v *= img_v
        img_v = np.where(img_v > 255, 255, img_v)
        img_v = img_v.astype(np.uint8)

        weight_h = 5
        weight_s = 1
        weight_v = 1

        img_better = cv2.addWeighted(img_s, weight_s, img_v, weight_v, 0)
        img_better = cv2.addWeighted(img_better, weight_s + weight_v, img_h, weight_h, 0)

        img_better = img_better.astype(np.uint8)
        img_better = cv2.blur(img_better, (8, 8))
        
        if debug:
            cv2.imshow('Source-H', img_h)
            cv2.imshow('Source-S', img_s)
            cv2.imshow('Source-V', img_v)
            cv2.imshow('Improved', img_better)
            
        return img_better

    @staticmethod
    def __calc_threshold(img, max_thresh_val=100):
        min_val = np.min(img)
        thresh = min(min_val + 0.3 * (255 - min_val), max_thresh_val)
        _, img_thresh = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((2, 2), np.uint8)
        img_thresh = cv2.morphologyEx(img_thresh, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((2, 2), np.uint8)
        img_thresh = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel)
        if debug:
            cv2.imshow('Improved Thresh', img_thresh)
        return img_thresh

    @staticmethod
    def __find_contour_in_mask(mask):
        edges, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        max_size = 0
        best_contour = None
        for c in edges:
            size = cv2.contourArea(c)
            if size > max_size:
                best_contour = c
                max_size = size
        return best_contour

    @staticmethod
    def __get_surrounding_rect(cnt):
        left = tuple(cnt[cnt[:, :, 0].argmin()][0])[0]
        right = tuple(cnt[cnt[:, :, 0].argmax()][0])[0]
        top = tuple(cnt[cnt[:, :, 1].argmin()][0])[1]
        bottom = tuple(cnt[cnt[:, :, 1].argmax()][0])[1]
        center_x = (right+left) / 2
        center_y = (bottom+top) / 2
        width = right - left
        height = bottom - top
        return (center_x, center_y), (width, height)

    def __to_centered_coordinates(self, point):
        h = self.img.shape[0]
        w = self.img.shape[1]
        x, y = point
        return x - w/2, y - h/2
