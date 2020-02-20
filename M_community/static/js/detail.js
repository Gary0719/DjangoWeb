$(function(){
    $("#comment_btn").click(function(){
        token = window.localStorage.getItem('community_token');
        username = window.localStorage.getItem('community_user');
        $.ajax({
            url:'/essay/comment',
            type:'post',
            contentType:'application/json;charset:utf-8',
            data:JSON.stringify({
                'comment':$('#my_comment').val(),
                'essay_id':$("#essay_id").text(),
                }),
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            dataType:'json',
            success:function(res){
                if (res.code == 200){
                    var user_comment = $('<div></div>').css({'width': '285px',
                                                             'height': '35px',
                                                             'border':'1px solid #666',
                                                             'margin': '0 auto',
                                                             'border-radius': '5px',
                                                             'margin-top': '10px',
                                                             'line-height': '35px',
                                                             'padding-left': '5px'}).html(res.data.username+' : '+res.data.comment);
                    $('#user_input').before(user_comment);
                    $("#my_comment").val('');
                }else if(res.code == 219){
                    alert('您当前未登录,请登陆后发表评论');
                    location.href = '/user/login';
                }else if(res.code == 220){
                    alert('您当前未登录,请登陆后发表评论');
                    location.href = '/user/login';
                }
            }
        })
    });
    $(".other_comment").click(function(){
        // console.log($(this).text().split(':')[0]);
        var prev_observer = $(this).text().split(':')[0];
        $("#my_comment").val('回复 '+prev_observer+' ');
    })
})