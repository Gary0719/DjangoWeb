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