window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        }
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

//     使用 Ajax 发送请求，因为这个 Editor 不属于 form 里面的内容
    $('#submit-btn').click(function(event) {
    //    禁止按钮的默认点击事件
        event.preventDefault();

        // 获取内容
        let title = $("input[name='title']").val();
        let category = $("#category-select").val();
        let content = editor.getHtml();
        // 因为是 post 请求，所以还需要csrf_token
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

        console.log({title, category, content, csrfmiddlewaretoken})

        // 提交请求
        $.ajax("/blog/pub", {
            method: "POST",
            data: {title, category, content, csrfmiddlewaretoken},
            success: function (result) {
                console.log(result)
                if (result['code'] == 200) {
                    window.location = '/blog/detail/' + result['data']['blog_id']
                } else {
                    alert(result['message'])
                }
            }
        })
    })
}