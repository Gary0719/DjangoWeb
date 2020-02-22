// 图片上传预览的函数:
function readURL(input){
    if (input.files && input.files[0]){
        var reader = new FileReader();
        reader.onload = function(e){
            $('#show').attr('src',e.target.result);
        }
        reader.readAsDataURL(input.files[0]); 
    }
} 
// 视频上传预览的函数:
function videoURL(input){
    if (input.files && input.files[0]){
        var reader = new FileReader();
        reader.onload = function(e){
            $('#myvideo').attr('src',e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}


$(function(){
    $('[name="essayPicture"]').change(function(){
        // 生成一个图片节点:
        img_show = $('<img id="show" class="hide">').css({
            'width': '300px',
            'height': '225px',
            'position': 'absolute',
            'right': '10px',
            'top': '36px',
            'border-radius': '5px',
            'border': 'none',
        });
        $("#pic").prepend(img_show);
        // 给图片节点设置src属性,并取消隐藏:
        readURL(this);
        img_show.toggleClass('hide');
        $("#plus_1").toggleClass('hide');
        // 生成一个重选按钮,并追加:
        reselect_btn = $("<button id='reselect'>重选</button>").css({
            'position': 'absolute',
            'right': '10px',
            'top': '10px',
            'width': '60px',
            'height': '21px',
            'line-height': '21px',
            'font-size': '13px',
            'border-radius': '5px',
            'z-index': '10',
            'cursor': 'pointer',
            'outline': 'none',
            'border': 'none',
            'color': '#fff',
            'background-color': '#c20c0b',
        });
        $("#pic").prepend(reselect_btn);
        reselect_btn.click(function(){
            // 点击重选时:预览图片移除;上传文件框重置;显示'+';重选按钮移除
            img_show.remove();
            $("#essayPicture").val(undefined);
            $("#plus_1").toggleClass('hide');
            reselect_btn.remove();
        })
    });

    $("#upload_video").change(function(){
        // 生成一个视频节点:
        video_show = $('<video id="myvideo" controls="controls" width="340" height="255" class="hide"></video>').css({
            'position': 'absolute',
            'right': '10px',
            'top': '5px',
            'outline': 'none'
        })
        $("#video_content").prepend(video_show);
        // 给视频节点设置src属性:
        videoURL(this);
        var timerId = setTimeout(function(){
            // 将视频节点移除隐藏属性; '+'号隐藏; 生成重选按钮并追加;
            $("#myvideo").toggleClass('hide');
            $("#plus").toggleClass('hide');
            var reselect_btn = $("<button id='reselect'>重选</button>").css({
                'position': 'absolute',
                'right': '10px',
                'top': '10px',
                'width': '60px',
                'height': '21px',
                'line-height': '21px',
                'font-size': '13px',
                'border-radius': '5px',
                'z-index': '10',
                'cursor': 'pointer',
                'outline': 'none',
                'border': 'none',
                'color': '#fff',
                'background-color': '#c20c0b',
            });
            $("#video_content").append(reselect_btn);
            $("#video_show").toggleClass('hide');
            reselect_btn.click(function(){
                // 点击重选按钮时: 将视频节点移除; 上传文件框重置; '+'号显示出来; 重选按钮移除
                video_show.remove();
                $("#upload_video").val(undefined);
                $("#plus").toggleClass('hide');
                reselect_btn.remove();
                $("#video_show").toggleClass('hide');
            })
        },2000);
        timerId;
        
    });


    $('#send').click(function(){
        formdata = new FormData();
        token = window.localStorage.getItem('community_token');
        username = window.localStorage.getItem('community_user');
        if (username && token){
            image_file = $("#essayPicture")[0].files[0];
            video_file = $("#upload_video")[0].files[0];
            text = $("#content_text").val();
            title = $("#essayTitle").val();
            select = $("#classify").val();
            formdata.append('image_file',image_file);
            formdata.append('video_file',video_file);
            formdata.append('text',text);
            formdata.append('title',title);
            formdata.append('select',select);
            formdata.append('username',username);
            formdata.append('token',token);
            // console.log(formdata.get('image_file'));
            // console.log(formdata.get('video_file'));
            // console.log(formdata.get('text'));
            // console.log(formdata.get('title'));
            // console.log(formdata.get('select'));
            if(image_file == undefined){
                alert('您还未选择专辑封面!');
            }else if(video_file == undefined){
                alert('您还未选择上传视频!');
            }else if(text.length == 0){
                alert('您还未添加相应描述!');
            }else if(title.length == 0){
                alert('您还未添加文章标题!');
            }else{
                $.ajax({
                    url:'/essay/post',
                    type:'post',
                    processData: false,
                    contentType: false,
                    data: formdata,
                    dataType:'json',
                    success:function(res){
                        if(res.code == 200){
                            alert(res.data);
                            location.href = '/index/';
                        }else{
                            alert(res.data);
                        }
                    },
                })
            }
        }else{
            alert('您当前为登录!');
        }
    })
}) 
