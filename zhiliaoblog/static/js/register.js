// 需要在页面加载完成执行函数
$(function () {
    // 按钮的点击事件回调 - 每次点击的时候都要重新绑定？
    function bindCaptchaBtnClick() {
        $('#captcha-btn').click(function () {
        // 将当前按钮的 js 对象转成 jQuery 对象
        let $this = $(this);
        // 获取输入的邮箱
        let email = $("input[name='email']").val();
        if (!email) {
            alert("请先输入邮箱！");
            return
        }
        // 取消按钮的点击事件
        $this.off("click");

        // 发送 Ajax 请求获取验证码
        $.ajax("/auth/captcha?email="+email, {
                method: 'GET',
                success: function (result) {
                    console.log(result)
                    if (result["code"] == 200) {
                        alert("验证码发送成功!");
                    } else {
                        alert(result["message"]);
                    }
                },
                fail: function (error) {
                    console.log(error)
                }
            })

        // 倒计时
        let countdown = 60
        // 创建定时器
        let timer = setInterval(function () {
            if (countdown <= 0) {
                $this.text("获取验证码")
                // 清除定时器
                clearInterval(timer)
                // 重新绑定点击事件
                bindCaptchaBtnClick();
            } else {
                $this.text(countdown + "s")
                countdown--;
            }
        }, 1000)


    })
    }

    bindCaptchaBtnClick()
})