/**
 * js网页雪花效果jquery插件
 */
(function ($) {

    $.fn.snow = function (options) {

        var $flake = $('<div id="snowbox" />').css({'position': 'absolute', 'top': '-50px'}).html('&#10052;'),
            documentHeight = $(document).height(),
            documentWidth = $(document).width(),
            defaults = {
                minSize: 10,		//雪花的最小尺寸
                maxSize: 20,		//雪花的最大尺寸
                newOn: 1000,		//雪花出现的频率
                flakeColor: "#FFFFFF"
            },
            options = $.extend({}, defaults, options);

        var interval = setInterval(function () {
            var startPositionLeft = Math.random() * documentWidth - 100,
                startOpacity = 0.5 + Math.random(),
                sizeFlake = options.minSize + Math.random() * options.maxSize,
                endPositionTop = documentHeight - 40,
                endPositionLeft = startPositionLeft - 100 + Math.random() * 500,
                durationFall = documentHeight * 10 + Math.random() * 5000;
            $flake.clone().appendTo('body').css({
                left: startPositionLeft,
                opacity: startOpacity,
                'font-size': sizeFlake,
                color: options.flakeColor
            }).animate({
                    top: endPositionTop,
                    left: endPositionLeft,
                    opacity: 0.2
                }, durationFall, 'linear', function () {
                    $(this).remove()
                }
            );

        }, options.newOn);

    };

})(jQuery);

    $(function () {
    $("#search").click(function (event) {
        event.preventDefault();
        var search_input = $("#content");
        var keyword = search_input.val();
        if(keyword=='' || keyword=='点击一下，你就知道'){
            zlalert.alertInfoToast('请输入查询的内容！');
            return ;
        }else if(keyword.indexOf("：")!=-1){   //判断字符串出现‘：’
            strs = keyword.split("：");
            value = strs[1];
            console.log(value);
            if (value.match(/^[ ]*$/)){
                zlalert.alertInfoToast('关键字不能为空！');
                return ;
            }
            else {
            window.location = "/search/?keyword=" + keyword
        }

        }
        else {
            window.location = "/search/?keyword=" + keyword
        }
    })
});