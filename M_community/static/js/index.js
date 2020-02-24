
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

$(function(){
    $('.myDomain:eq(0)')[0].onmouseover = function(){
        $('#myEssay').removeClass('hide');
        $('#myChat').addClass('hide');
        $('#myLike').addClass('hide');
    };
    $('#myEssay')[0].onmouseover=function(){
        $('#myEssay').removeClass('hide');
    };
    $('#myEssay')[0].onmouseout=function(){
        $('#myEssay').addClass('hide');
    };

    $('.myDomain:eq(1)')[0].onmouseover = function(){
        $('#myChat').removeClass('hide');
        $('#myEssay').addClass('hide');
        $('#myLike').addClass('hide');
    };
    $('#myChat')[0].onmouseover=function(){
        $('#myChat').removeClass('hide');
    };
    $('#myChat')[0].onmouseout=function(){
        $('#myChat').addClass('hide');
    };

    $('.myDomain:eq(2)')[0].onmouseover = function(){
        $('#myLike').removeClass('hide');
        $('#myEssay').addClass('hide');
        $('#myChat').addClass('hide');
    };
    $('#myLike')[0].onmouseover=function(){
        $('#myLike').removeClass('hide');
    };
    $('#myLike')[0].onmouseout=function(){
        $('#myLike').addClass('hide');
    };
});

$(function(){
    //2秒轮播一次
    var index = 1;
    var timer = setInterval(function () {
        $(".slide_img").eq(index).removeClass('the_hide').siblings('.slide_img').addClass('the_hide');
        index = (index == 6) ? 0 : index + 1;
    }, 2000);
});

$(function(){
    // 总消息数:
    var allmessage = 0;
    // 新的好友申请消息数:
    var newfriendmessage = 0;
    // 新的留言数量:
    var newmessage = 0;

    token = window.localStorage.getItem('community_token');
    username = window.localStorage.getItem('community_user');

    $.ajax({
        url:'/letter/myletter',
        type:'get',
        dataType:'json',
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", token);
        },
        success:function(res){
            if(res.code == 283){
                for(var i=0;i<res.data.length;i++){
                    // console.log(res.data[0][i]);
                    newfriendmessage++;
                }
                
                allmessage = newfriendmessage;
                // console.log(allmessage);
                
                // 新的好友提醒:
                var newFriendRemaid=$("<div id='newfriend'></div>").html(newfriendmessage).css({
                    'width':'14px',
                    'height':'14px',
                    'text-align': 'center',
                    'line-height':'14px',
                    'border-radius': '50%',
                    'position': 'absolute',
                    'top': '52px',
                    'right': '2px',
                    'font-size':'10px',
                    'color':'#fff',
                    'background-color': 'rgba(194, 12, 11, 0.7)',

                });
                $("#myChat").append(newFriendRemaid);
                newRemaid = $("<div id='newfriend'></div>").html(allmessage).css({
                    'width':'14px',
                    'height':'14px',
                    'text-align': 'center',
                    'line-height':'14px',
                    'border-radius': '50%',
                    'position': 'absolute',
                    'top': '71px',
                    'right': '8px',
                    'font-size':'10px',
                    'color':'#fff',
                    'background-color': 'rgba(194, 12, 11, 0.7)',

                });
                // console.log(allmessage);
                $("#user").append(newRemaid);
            }
        }
    })
    $.ajax({
        url:'/letter/myletter_1',
        type:'get',
        dataType:'json',
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", token);
        },
        success:function(res){
            if(res.code == 200){
                newmessage+=res.data;
                var newLetterRemaid=$("<div id='newletter'></div>").html(newmessage).css({
                    'width':'14px',
                    'height':'14px',
                    'text-align': 'center',
                    'line-height':'14px',
                    'border-radius': '50%',
                    'position': 'absolute',
                    'top': '16px',
                    'right': '2px',
                    'font-size':'10px',
                    'color':'#fff',
                    'background-color': 'rgba(194, 12, 11, 0.7)',

                });
                $("#myChat").append(newLetterRemaid);

                allmessage += newmessage;
                newRemaid = $("<div id='newfriend'></div>").html(allmessage).css({
                    'width':'14px',
                    'height':'14px',
                    'text-align': 'center',
                    'line-height':'14px',
                    'border-radius': '50%',
                    'position': 'absolute',
                    'top': '71px',
                    'right': '8px',
                    'font-size':'10px',
                    'color':'#fff',
                    'background-color': 'rgba(194, 12, 11, 0.7)',

                });
                // console.log(allmessage);
                $("#user").append(newRemaid);
            }
        }
    })
})

$(function(){
    $("#newfriends").click(function(){
        token = window.localStorage.getItem('community_token');
        username = window.localStorage.getItem('community_user');
        if(token && username){
            location.href='/letter/newfriends/'+username;
        }else{
            alert('您当前未登录');
        }
        
    })

    $("#myfriends").click(function(){
        token = window.localStorage.getItem('community_token');
        username = window.localStorage.getItem('community_user');
        if(token && username){
            location.href='/letter/myfriends/'+username;
        }else{
            alert('您当前未登录');
        }
        
    })

    // $("#news").click(function(){
    //     token = window.localStorage.getItem('community_token');
    //     username = window.localStorage.getItem('community_user');
    //     if(token && username){
    //         location.href='/letter/news?user='+username;
    //     }else{
    //         alert('您当前未登录');
    //     }
        
    // })
})