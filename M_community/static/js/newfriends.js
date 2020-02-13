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
});

$(function(){
    $(".agree").click(function(){
        name = $(this).parent().siblings('#friend_name').html();
        // console.log(name);
        token = window.localStorage.getItem('community_token');
        username = window.localStorage.getItem('community_user');
        $.ajax({
            url:'/letter/newfriends/'+username,
            type:'post',
            contentType:'application/json;charset:utf-8',
            dataType:'json',
            data:JSON.stringify({
                'option':'1',
                'agree_friend':name,
            }),
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success:function(res){
                if(res.code == 200){
                    alert(res.data);
                    location.reload();
                }else if(res.code == 281){
                    alert(res.data);
                    location.reload();
                }else if(res.code == 291){
                    alert(res.data);
                    location.reload();
                }
            }
        })
    })

    $(".ignore").click(function(){
        name = $(this).parent().siblings('#friend_name').html();
        console.log(name);
        token = window.localStorage.getItem('community_token');
        username = window.localStorage.getItem('community_user');
        $.ajax({
            url:'/letter/newfriends/'+username,
            type:'post',
            contentType:'application/json;charset:utf-8',
            dataType:'json',
            data:JSON.stringify({
                'option':'0',
                'ignore_friend':name,
            }),
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success:function(res){
                if(res.code == 200){
                    alert(res.data);
                    location.reload();
                }else if(res.code == 281){
                    alert(res.data);
                    location.reload();
                }else if(res.code == 291){
                    alert(res.data);
                    location.reload();
                }
            }
        })
    })
})