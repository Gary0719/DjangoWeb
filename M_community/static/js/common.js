$(function(){
    var username = window.localStorage.getItem('community_user');
    var head_portrait = window.localStorage.getItem('head_portrait');
    if (username){
        $('#tools>div:eq(1)').toggleClass('hide');
        $('#tools a:eq(2)').html(username);
        $("#head").toggleClass('hide');
        $('#tools>div:eq(0)').toggleClass('hide');
        $("#head").attr('src',head_portrait).css({'width': '60px',
                                                  'height': '60px',
                                                  'border-radius':'15px',
                                                  'position': 'absolute',
                                                  'right': '28px',
                                                  'top': '30px',})
    }
    $('#tools a:eq(3)').click(function(){
        localStorage.removeItem('community_user');
        localStorage.removeItem('community_token');
        localStorage.removeItem('head_portrait');
        location.reload();
    })
    $("#head")[0].onmouseover = function(){
        url =  $('#head').prop('src');
        if (url == 'http://127.0.0.1:8000/static/image/default_head.jpg'){
            head_tip = $('<span>欢迎来到喵社区~这只喵是您的初始头像,点击用户名更换属于您的专属头像吧~</span>').css({
                'display': 'inline-block',
                'width': '250px',
                'padding-left': '3px',
                'padding-right': '3px',
                'border-radius': '5px',
                'position': 'absolute',
                'right': '100px',
                'top': '40px',
                'font-size': '14px',
                'background-color': 'rgba(0, 0, 0, 0.3)',
                'color': '#fff',
            });
            $("header").append(head_tip);
            $("#head")[0].onmouseout = function(){
                head_tip.remove();
            }
        }
    };
});