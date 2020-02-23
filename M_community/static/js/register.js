$(function(){
    $('#sure').click(function(){
        $.ajax({
            url:'/user/register',
            type:'post',
            contentType:'application/json;charset:utf-8',
            data:JSON.stringify({
                'username':$('[name="username"]').val(),
                'password_1':$('[name="password_1"]').val(),
                'password_2':$('[name="password_2"]').val(),
                'gender':$('[name="gender"]').val(),
                'email':$('[name="email"]').val(),
            }),
            dataType:'json',
            success:function(res){             
                if (res.code == 200){
                    user_name = res.data.username;
                    com_token = res.data.token;
                    head_img = res.data.head;
                    localStorage.setItem('community_user',user_name);
                    localStorage.setItem('community_token',com_token);
                    localStorage.setItem('head_portrait', head_img);
                    window.alert('激活邮件已发送至您的邮箱,请注意查收!');
                    location.href='/index';
                }else if(res.code == 201){
                    $('#show_tip_1').css('display','block').text(res.data).css('color','#fff');
                }else if(res.code == 202){
                    $('#show_tip_2').css('display','block').text(res.data).css('color','#fff');
                }else if(res.code == 203){
                    $('#show_tip_3').css('display','block').text(res.data).css('color','#fff');
                }else if(res.code == 204){
                    $('#show_tip_4').css('display','block').text(res.data).css('color','#fff');
                }else if(res.code == 205){
                    $('#show_tip_1').css('display','block').text(res.data).css('color','#fff');
                }
                else if(res.code == 206){
                    $('#show_tip_3').css('display','block').text(res.data).css('color','#fff');
                }
                else if(res.code == 207){
                    $('#show_tip_2').css('display','block').text(res.data).css('color','#fff');
                }else if(res.code == 208){
                    $('#show_tip_4').css('display','block').text(res.data).css('color','#fff');
                }else if(res.code == 209){
                    $('#show_tip_1').css('display','block').text(res.data).css('color','#fff');
                }
            }
        })
    })
})