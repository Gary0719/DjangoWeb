$(function(){
    $("#search").click(function(){
        $.ajax({
            url:'/letter/friend',
            type:'post',
            contentType:'application/json;charset:utf-8',
            dataType:'json',
            data:JSON.stringify({
                'friend_name':$("#friend_name").val()
            }),
            success:function(res){
                if(res.code == 270){
                    $("#tip").removeClass('hiden').html(res.data);
                }else if(res.code == 271){
                    $("#tip").removeClass('hiden').html(res.data);
                }else if(res.code == 200){
                    $("#tip").addClass('hiden');
                    // 生成好友资料卡,并添加该节点
                    var card=$("<div id='card'></div>").css({'width': '400px',
                                                   'height': '320px',
                                                   'border': '1px solid #666',
                                                   'border-radius': '5px',
                                                   'position': 'absolute',
                                                   'left': '25px',
                                                   'bottom': '20px'});
                    $("#find").after(card);

                    // 加载好友头像,并添加该节点
                    var head=$("<img id='head'>").css({'width': '100px',
                                              'height': '100px',
                                              'position': 'absolute',
                                              'left': '150px',
                                              'top': '20px',
                                              'border-radius': '50px',}).prop('src',res.data[2]);
                    $("#card").prepend(head);

                    // 加载好友昵称,并添加该节点
                    var name=$("<div id='name'></div>").css({'width':'200px',
                                                   'height':'30px',
                                                   'text-align': 'center',
                                                   'position': 'absolute',
                                                   'left': '100px',
                                                   'top': '135px',
                                                   'font-size':'16px',
                                                   'font-weight': '900',
                                                   'line-height':'30px'}).html(res.data[0]);
                    $("#head").after(name);

                    // 加载好友性别,并添加该节点
                    var gender=$("<div id='gender'></div>").css({'width':'200px',
                                                     'height':'30px',
                                                     'text-align': 'center',
                                                     'line-height':'30px',
                                                     'position': 'absolute',
                                                     'left': '100px',
                                                     'top': '180px',
                                                     'font-size':'16px'}).html(res.data[1])
                    $("#name").after(gender);

                    // 加载添加好友的按钮,并添加该节点
                    var add_btn=$("<button id='add'>添加好友</button>").css({'border': 'none',
                                                                            'outline': 'none',
                                                                            'width': '90px',
                                                                            'height': '30px',
                                                                            'color': '#fff',
                                                                            'background-color':'#4080e2',
                                                                            'border-radius': '5px',
                                                                            'cursor': 'pointer',
                                                                            'position': 'absolute',
                                                                            'bottom': '20px',
                                                                            'right': '75px',});
                    $("#gender").after(add_btn);

                    // 加载重新搜索的按钮,并添加该节点
                    var reload_btn=$("<button id='reload'>重新搜索</button>").css({'border': 'none',
                                                                            'outline': 'none',
                                                                            'width': '90px',
                                                                            'height': '30px',
                                                                            'color': '#fff',
                                                                            'background-color':'#30c37f',
                                                                            'border-radius': '5px',
                                                                            'cursor': 'pointer',
                                                                            'position': 'absolute',
                                                                            'bottom': '20px',
                                                                            'left': '75px',});
                    $("#add").after(reload_btn);

                    $("#reload").click(function(){
                        location.reload();
                    })
                    $("#add").click(function(){
                        token = window.localStorage.getItem('community_token');
                        username = window.localStorage.getItem('community_user');
                        $.ajax({
                            url:'/letter/newfriend',
                            type:'post',
                            contentType:'application/json;charset:utf-8',
                            dataType:'json',
                            data:JSON.stringify({
                                'target_friend':res.data[0],
                            }),
                            beforeSend: function(request) {
                                request.setRequestHeader("Authorization", token);
                            },
                            success:function(res){
                                if(res.code == 200){
                                    alert(res.data);
                                    location.reload();
                                }else if(res.code == 220){
                                    alert(res.data);
                                    location.href = '/user/login';
                                }else if(res.code == 272){
                                    alert(res.data);
                                    location.reload();
                                }else if(res.code == 273){
                                    alert(res.data);
                                    location.reload();
                                }else if(res.code == 274){
                                    alert(res.data);
                                    location.reload();
                                }
                            }
                        })
                    })
                }
            }
        })
    })
    
})