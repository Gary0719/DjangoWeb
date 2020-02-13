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
    $('#head_portrait').change(function(){
        readURL(this);
    });

    $("button").click(function(){
        token = window.localStorage.getItem('community_token');
        username = window.localStorage.getItem('community_user');
        formdata = new FormData();
        formdata.append("image",$("#head_portrait")[0].files[0]);
        $.ajax({
            url:'/user/upload',
            processData: false,
            contentType: false,
            type: 'post',
            data: formdata,
            dataType:'json',
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success:function(res){
                if(res.code == 200){
                    localStorage.setItem('head_portrait',res.data[1])
                    alert(res.data[0]);
                    location.href='/index/';
                }
            }
        })
    })
})
