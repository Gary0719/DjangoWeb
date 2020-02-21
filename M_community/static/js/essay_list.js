$(function(){
    token = window.localStorage.getItem('community_token');
    username = window.localStorage.getItem('community_user');
    $.ajax({
        url: '/essay/essay_data',
        type: 'get',
        dataType:'json',
        beforeSend: function(request) {
                    request.setRequestHeader("Authorization", token);
        },
        success:function(res){
            if (res.code == 200){
                essayList = res.data;
                for(var i=0; i<essayList.length; i++){
                    console.log(essayList[i]);
                }
            }else{
                alert(res.data);
            }
        }
    })
})