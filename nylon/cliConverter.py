from colorama import Fore, Back, Style
import shutil
import numpy as np
import colorsys
import cv2
import sys
import time
from os import system, name


class terminalColor:
    def __init__(self, code, name, r, g, b):
        self.code = code
        self.name = name
        self.r = r
        self.g = g
        self.b = b


# 画像をコンソールへ標準出力可能な形式へ変換
class cliConverter:
    def __init__(self, pixelChar="  "):
        self.pixelChar = pixelChar

        self.terminalColors = [
            terminalColor(Back.BLACK, "black", 0, 0, 0),
            terminalColor(Back.LIGHTBLACK_EX, "light black", 102, 102, 102),
            terminalColor(Back.BLUE, "blue", 37, 114, 200),
            terminalColor(Back.LIGHTBLUE_EX, "light blue", 59, 142, 235),
            terminalColor(Back.CYAN, "cyan", 67, 169, 205),
            terminalColor(Back.LIGHTCYAN_EX, "light cyan", 75, 184, 219),
            terminalColor(Back.GREEN, "green", 85, 189, 122),
            terminalColor(Back.LIGHTGREEN_EX, "light green", 95, 209, 139),
            terminalColor(Back.MAGENTA, "magenta", 188, 66, 188),
            terminalColor(Back.LIGHTMAGENTA_EX,
                          "light magenta", 214, 112, 214),
            terminalColor(Back.RED, "red", 205, 49, 49),
            terminalColor(Back.LIGHTRED_EX, "light red", 238, 75, 75),
            terminalColor(Back.WHITE, "white", 229, 229, 229),
            terminalColor(Back.LIGHTWHITE_EX, "light white", 250, 250, 250),
            terminalColor(Back.YELLOW, "yellow", 229, 229, 73),
            terminalColor(Back.LIGHTYELLOW_EX, "light yellow", 245, 245, 579),
        ]

    # TerminalImageのピクセルを返す
    def pixel(self, colorCode: str):
        return colorCode + self.pixelChar + Back.RESET

    # 標準出力で利用可能な色のまとめ
    def colorExamples(self):
        exampleStr = ""

        for tColor in self.terminalColors:
            code = tColor.code
            name = tColor.name

            exampleStr += "{} {} {}\n".format(
                self.pixel(code), name, Back.RESET)

        return exampleStr

    # コンソールをクリア
    def clearConsole(self):
        # window
        if name == 'nt':
            _ = system('cls')
        # mac, linux
        else:
            _ = system('clear')

    # terminalImage: Back.{colorName}の二次元配列
    def terminalImageToStr(self, terminalImage):
        tImageHeight, tImageWidth = len(terminalImage), len(terminalImage[0])
        imgStr = ""

        for i in range(tImageHeight):
            row = ""

            for j in range(tImageWidth):
                row += self.pixel(terminalImage[i][j])

            imgStr += row + "\n"

        return imgStr

    # rgb: 0〜250
    # hue: 0〜360

    def rgbToHue(self, r, g, b):
        # rgb値を0〜1の範囲にキャストして渡す
        hue = colorsys.rgb_to_hsv(r/255, g/255, b/255)[0]
        # hueを0〜360の範囲にキャスト
        return hue * 360

    # 色差を算出
    def colorDistance(self, r, g, b, r2, g2, b2):
        rDistance = abs(r - r2)
        gDistance = abs(g - g2)
        bDistance = abs(b - b2)

        averageDistance = (rDistance + gDistance + bDistance) / 3
        return averageDistance

    # rgbを標準出力が対応している色へ変換
    def rgbToTerminalColor(self, r, g, b):
        colorDistancess = []

        # 各ターミナルカラーとの色差を算出
        for tColor in self.terminalColors:
            r2, g2, b2 = tColor.r, tColor.g, tColor.b
            distance = self.colorDistance(r, g, b, r2, g2, b2)
            code = tColor.code

            colorDistancess.append(distance)

        minColorDistanceIndex = colorDistancess.index(min(colorDistancess))

        return self.terminalColors[minColorDistanceIndex]

    def terminalSize(self):
        size = shutil.get_terminal_size()
        width = size.columns
        height = size.lines - 1

        return width, height

    # ターミナルへ画像をフィットさせた場合のサイズを返す: 横幅, 縦幅
    def fitedTerminalImageSize(self, img):
        imgHeight, imgWidth = img.shape[:2]
        terminalWidth, terminalHeight = self.terminalSize()
        imgRatio = imgHeight / imgWidth

        widthRatio = terminalWidth / imgWidth
        heightRatio = terminalHeight / imgHeight

        terminalWidthFitedSize = terminalWidth, int(
            imgHeight * widthRatio)

        terminalHeightFitedSize = int(
            imgWidth * heightRatio), terminalHeight

        terminalWidthFitedArea = terminalWidthFitedSize[0] * \
            terminalWidthFitedSize[1]

        terminalHeightFitedArea = terminalHeightFitedSize[0] * \
            terminalHeightFitedSize[1]

        # ターミナル内に収まるサイズを返す
        if terminalWidthFitedArea > terminalHeightFitedArea:
            return terminalHeightFitedSize
        else:
            return terminalWidthFitedSize

    # img: numpy画像
    # 画像をTerminalImageへ変換
    def imageToTerminalImage(self, img, height=None, width=None):
        imgHeight, imgWidth = img.shape[:2]

        if height is None or width is None:
            terminalImageSize = self.fitedTerminalImageSize(img)
        else:
            terminalImageSize = width, height

        resizedImage = cv2.resize(
            img, (terminalImageSize[0], terminalImageSize[1]))

        terminalImage = []

        for i in range(terminalImageSize[1]):
            row = []

            for j in range(terminalImageSize[0]):
                b, g, r = resizedImage[i][j]
                tColor = self.rgbToTerminalColor(r, g, b)
                row.append(tColor.code)

            terminalImage.append(row)

        return terminalImage
