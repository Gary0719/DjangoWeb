$(function(){
    var token = window.localStorage.getItem('community_token');
    var username = window.localStorage.getItem('community_user');
    $.ajax({
        url:'/letter/news/data',
        type:'get',
        dataType:'json',
        beforeSend:function(request) {
            request.setRequestHeader("Authorization", token);
        },
        success:function(res){
            if(res.code == 200){
                var main = $("#main");
                console.log(res.data[0].length);
                if(res.data[0].length>0){
                    for(var i=0;i<res.data[0].length;i++){
                        friend_name = res.data[0][i];
                        friend_head_url = res.data[1][friend_name][1];
                        friend_message_num = res.data[1][friend_name][0];
                        // console.log(friend_name);
                        // console.log(friend_head_url);
                        // console.log(friend_message_num);
                        one = $('<div class="oneNewMessage"></div>').css({
                            'position': 'relative',
                            'border': '1px solid #666',
                            'border-radius': '12px',
                            'width': '1000px',
                            'height': '120px',
                            'margin-top': '15px',
                            'margin-left': '25px',
                            'margin-right': '25px',
                        });
                        uname = $('<span class="uname">'+friend_name+'</span>').css({
                            'display': 'inline-block',
                            'position': 'absolute',
                            'left': '130px',
                            'top': '12px',
                            'font-size': '20px',
                            'color': '#4080e2',
                            'font-weight': '900',
                        });
                        photo = $('<img src="" alt="">').attr('src',friend_head_url).css({
                            'position': 'absolute',
                            'left': '10px',
                            'top': '10px',
                            'width': '100px',
                            'height': '100px',
                            'border-radius': '10px',
                        });
                        tip = $('<div class="tip">新消息数:</div>').css({
                            'position': 'absolute',
                            'left': '130px',
                            'top': '50px',
                            'font-size': '16px',
                            'color': '#666',
                        });
                        num = $('<div class="num"></div>').html(friend_message_num).css({
                            'position': 'absolute',
                            'left': '210px',
                            'top': '52px',
                            'text-align': 'center',
                            'line-hight':'14px',
                            'color': '#c20c0b',
                            'font-size': '16px',
                        });
                        btn = $('<button class="go">前往查看</button>').css({
                            'position': 'absolute',
                            'right': '20px',
                            'top': '47px',
                            'border': 'none',
                            'outline': 'none',
                            'width': '70px',
                            'height': '30px',
                            'color': '#fff',
                            'background-color':'#4080e2',
                            'border-radius': '5px',
                            'cursor': 'pointer',
                        });
                        one.prepend(uname);
                        uname.after(photo);
                        photo.after(tip);
                        tip.after(num);
                        num.after(btn);
                        main.append(one);
    
                    }
                    $(".go").click(function(){
                        var friend = $(this).siblings('.uname').html();
                        console.log(friend);
                        // 点击 前往查看 按钮,向后端获取用户与当前好友聊天记录的url
                        $.ajax({
                            url:'/letter/with/'+friend,
                            type:'get',
                            dataType:'json',
                            beforeSend:function(request) {
                                request.setRequestHeader("Authorization", token);
                            },
                            success:function(res){
                                if(res.code == 200){
                                    // 如果成功获取该url,向后端发起更新服务器资源的请求
                                    // 把is_read字段更新为TRUE
                                    var url = res.data;
                                    $.ajax({
                                        url:'/letter/PATCH/news/'+username,
                                        type:'patch',
                                        contentType:'application/json;charset:utf-8',
                                        dataType:'json',
                                        beforeSend:function(request) {
                                            request.setRequestHeader("Authorization", token);
                                        },
                                        data:JSON.stringify({
                                            'friend':friend,
                                            'is_read':true,
                                        }),
                                        success:function(res){
                                            if (res.code == 200){
                                                console.log(res.data);
                                                // 如果更新成功,定位到与该好友的url
                                                location.href = url;
                                            }
                                        }
                                    })
                                    
                                }else{
                                    alert(res.data);
                                }
                            }
    
                        })
                        
                    })
                }else{
                    reminder = $('<div id="reminder"></div>').css({
                        'position': 'relative',
                        'width': '480px',
                        'height': '270px',
                        // 'border': '1px solid #666',
                        'border-radius': '10px',
                        'margin': '0 auto',
                        'margin-top': '30px',
                        'background-image': "url('/static/image/none.jpg')",
                        'background-size': 'cover',
                        'opacity': '0.8',
                    });
                    content = $('<span id="con">目前没有新的好友消息哦~</span>').css({
                        'position': 'absolute',
                        'display': 'inline-block',
                        'width': '220px',
                        'height': '27px',
                        'font-size': '18px',
                        'font-weight':'900',
                        'text-align': 'center',
                        'left': '130px',
                        'top': '120px',
                        'color':'#fff',
                        'opacity': '1',
                    });
                    reminder.prepend(content);
                    main.prepend(reminder);
                }
            }else if (res.code == 281){
                location.href = '/user/login';
            }
        }
    });
})
