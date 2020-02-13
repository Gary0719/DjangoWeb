var querystring = location.search
window.onload=function(){
// 后端回复224,跳转绑定
    $.ajax({
        url: '/user/weibo/users'+querystring,
        type: 'get',
        dataType: "json",
        success: function (res) {
            console.log(res);
            if (res.code == 200) {
                window.localStorage.clear();
                localStorage.setItem('community_user',res.data.username);
                localStorage.setItem('community_token',res.data.token);
                setTimeout(()=>{
                    window.location.href="/index/";
                },3000)
            }else if(res.code == 225){
                // 跳转页面,实现本网站与微博账号的绑定
                access_token = res.access_token
                uid = res.uid
            }else if(res.code == 224){
                localStorage.setItem('weibo_uid',res.uid);
                location.href='/user/bind';
                // 将微博用户的id 存到本地存储,并跳转账号绑定页面
            }
        }
    });
}