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