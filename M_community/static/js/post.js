function readURL(input){
    if (input.files && input.files[0]){
        var reader = new FileReader();
        reader.onload = function(e){
            $('#show').css('display','block').attr('src',e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
        // $('[name="photo"]').attr('style','display:none');
    }
}  
$(function(){
    $('[name="essayPicture"]').change(function(){
        readURL(this);
    });

    $('#send').click(function(){
        token = window.localStorage.getItem('community_token');
        username = window.localStorage.getItem('community_user');
        formdata = new FormData();
        formdata.append("image",$("#essayPicture")[0].files[0]);
        $.ajax({
            url:'/essay/post',
            type:'put',
            contentType:'application/json;charset:utf-8',
            data:JSON.stringify({
                'title':$('#essayTitle').val(),
                'classify':$('#classify').val(),
                'content_text':$('#content_text').val(),
                }),
            dataType:'json',
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(res) {
                if (res.code == 200) {
                    $.ajax({
                        processData: false,
                        contentType: false,
                        url: '/essay/post',
                        type: 'post',
                        data: formdata,
                        dataType:'json',
                        beforeSend: function(request) {
                            request.setRequestHeader("Authorization", token);
                        },
                        success: function(res) {
                            if (res.code == 200) {
                                alert('成功！')
                                location.href = '/index';
                            }else if(res.code == 224){
                                alert(res.data);
                            }
                        }
                    });
                }else if(res.code == 219){
                    alert('当前未登录');
                    location.href == '/user/login'
                }else if(res.code == 220){
                    alert('当前未登录');
                    location.href == '/user/login'
                }else if(res.code == 221){
                    alert(res.data);
                }else if(res.code == 222){
                    alert(res.data);
                }else if(res.code == 223){
                    alert(res.data);
                }
            },
        })
        
    })
}) 
