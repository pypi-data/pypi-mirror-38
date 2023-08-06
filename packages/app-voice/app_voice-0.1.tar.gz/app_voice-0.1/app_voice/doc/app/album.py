#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： album.py
#   @Author：    Enoch.Xiang
#   @contact：   xiangwenzhuo@yeah.net
#   @date：      18-7-19 下午4:11
#   @version：   1.0
# -------------------------------------------------
#   @Description :
#
#
# -------------------------------------------------


def delpoi():
    """
    @api {post} /delpoi 删除收藏
    @apiVersion 0.1.0
    @apiGroup Collect
    @apiDescription 删除收藏

    @apiParam {Float} timestamp 时间戳
    @apiParam {String} location 经纬度

    @apiSuccess {String} data 成功标识

    @apiSuccessExample {json} Success-Response:
    {
        "data": "Success.",
        "req_id": "r_049b93db7754407bb872aaee3d28f352",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }

    @apiError 21020  No poi_id in the request params

    @apiErrorExample {json} Error-Response:
    {
        "err_resp": {
            "code": "21020",
            "msg": "No poi_id in the request params!"
        },
        "req_id": "r_da328a55dfbc46bda249122030b8677d"
    }
    """
