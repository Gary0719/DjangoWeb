$(function(){
    $(".chat").click(function(){
        // console.log($(this).siblings(".name").html());
        var friend_name = $(this).siblings(".name").html();
        token = window.localStorage.getItem('community_token');
        username = window.localStorage.getItem('community_user');
        $.ajax({
            url:'/letter/with/'+friend_name,
            type:'get',
            dataType:'json',
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success:function(res){
                if (res.code == 200){
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
                            'friend':friend_name,
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
                }else if (res.code == 281){
                    alert(res.data);
                }
            }
        })
    })
})