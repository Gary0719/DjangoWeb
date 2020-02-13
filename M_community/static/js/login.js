$(function(){
    $('#sure').click(function(){
        $.ajax({
            url:'/user/login',
            type:'post',
            contentType:'application/json;charset:utf-8',
            data:JSON.stringify({
                'username':$('#username').val(),
                'password':$('#password_1').val(),
            }),
            dataType:'json',
            success:function(res){
                if (res.code == 200){
                    localStorage.setItem('community_user',res.data.username);
                    localStorage.setItem('community_token',res.data.token);
                    localStorage.setItem('head_portrait',res.data.head);
                    window.alert('登陆成功!');
                    location.href = '/index'
                }else if (res.code == 216){
                    $('#show_tip_1').css('display','block').text(res.data).css('color','#fff');
                }else if (res.code == 217){
                    $('#show_tip_2').css('display','block').text(res.data).css('color','#fff');
                }else if (res.code == 218){
                    $('#show_tip_1').css('display','block').text(res.data).css('color','#fff');
                    $('#show_tip_2').css('display','block').text(res.data).css('color','#fff');
                }
            }
        })
    })
    $("#weibo img").click(function(){
        $.ajax({
            url:'/user/weibo/authorization',
            type:'get',
            // contentType:'application/json;charset:utf-8',
            dataType:'json',
            success:function(res){
                if (res.code == 200){
                    location.href=res.oauth_url;
                }
            }
        })
    })
})