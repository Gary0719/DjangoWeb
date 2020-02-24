// 删除指定文章的函数:
function delete_essay(essay_id,token){
    // console.log(essay_id);
    $.ajax({
        url:'/essay/delete',
        type: 'post',
        contentType:'application/json;charset:utf-8',
        dataType:'json',
        data:JSON.stringify({
            'essay_id':essay_id,
        }),
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", token);
        },
        success:function(res){
            if (res.code = 200){
            }
            else{
                alert(res.data);
            }
        }
    })
}

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
                main = $("#main");
                essayList = res.data;
                for(var i=0; i<essayList.length; i++){
                    essay_id = essayList[i].essay_id;
                    essay_title = essayList[i].essay_title;
                    classify = essayList[i].classify;
                    click_rate = essayList[i].click_rate;
                    create_time = essayList[i].create_time.substring(0,10);
                    image = essayList[i].image;
                    one_essay = $('<div class="one_essay"></div>').css({
                        'border': '2px solid #666',
                        'border-radius': '10px',
                        'width': '300px',
                        'height': '300px',
                        'float': 'left',
                        'margin-top': '10px',
                        'margin-left': '23px',
                        'margin-right': '23px',
                        'position': 'relative',
                    });
                    essayId = $('<span class="essay_id"></span>').html(essay_id).css({
                        'display': 'none',
                    });
                    essayTitle = $('<span class="essay_title"></span>').html(essay_title).css({
                        'display': 'inline-block',
                        'width': '280px',
                        'font-size': '15px',
                        'font-weight': '600',
                        'position': 'absolute',
                        'top': '5px',
                        'left': '20px',
                    });
                    essayClassify = $('<span class="essay_classify"></span>').html('分类:' + classify).css({
                        'display': ' inline-block',
                        'font-size': '14px',
                        'position': 'absolute',
                        'bottom': '45px',
                        'left': '25px',
                        'color': '#4080e2',
                    });
                    essayClickRate = $('<span class="essay_click"></span>').html('点击率:' + click_rate).css({
                        'display': ' inline-block',
                        'font-size': '14px',
                        'position': 'absolute',
                        'bottom': '20px',
                        'left': '157px',
                        'color':'#666',
                    });
                    essayCreateTime = $('<span class="essay_create_time"></span>').html('发布时间:' + create_time).css({
                        'display': ' inline-block',
                        'font-size': '14px',
                        'position': 'absolute',
                        'bottom': '45px',
                        'right': '25px',
                        'color':'#666',
                    });
                    essayImage = $(' <img src="" class="essay_image">').attr('src',image).css({
                        'width': '260px',
                        'height': '195px',
                        'border-radius': '5px',
                        'position': 'absolute',
                        'top': '35px',
                        'left': '20px',
                        'cursor': 'pointer',
                    });
                    delete_button = $('<button class="del">删除日记</button>').css({
                        'width': '72px',
                        'height': '24px',
                        'position': 'absolute',
                        'bottom': '18px',
                        'left': '20px',
                        'cursor': 'pointer',
                        'border': 'none',
                        'outline': 'none',
                        'border-radius': '5px',
                        'background-color': '#c20c0b',
                        'color':'#fff',
                    })
                    one_essay.append(essayId);
                    one_essay.append(essayTitle);
                    one_essay.append(essayClassify);
                    one_essay.append(essayClickRate);
                    one_essay.append(essayCreateTime);
                    one_essay.append(essayImage);
                    one_essay.append(delete_button);
                    main.append(one_essay);

                    // 点击帖子图片时,跳转获取详情页:
                    essayImage.click(function(){
                        this_id = $(this).siblings('.essay_id').html();
                        location.href = '/essay/detail/' + username + '/' + this_id;
                    });
                    // 点击删除按钮时, 删除当前帖子:
                    delete_button.click(function(){

                        this_id = $(this).siblings('.essay_id').html();
                        delete_essay(this_id,token);
                        alert('当前文章已删除!');
                        location.reload();
                    })
                }
                if (res.data.length == 0){
                    reminder = $('<div id="reminder"></div>').css({
                        "background-image": "url('/static/image/none.jpg')",
                        "width": '480px',
                        'height': '270px',
                        'background-size': 'cover',
                        'margin': '0 auto',
                        'position': 'relative',
                        'opacity': '0.8',
                        'border-radius': '10px',
                    });
                    text = $('<span>您还没有发布文章呢~</span>').css({
                        'display': 'inline-block',
                        "width": '220px',
                        'height': '27px',
                        'font-size': '18px',
                        'font-weight': '900',
                        'text-align': 'center',
                        'opacity': '1',
                        'color': '#fff',
                        'position': 'absolute',
                        'left': '130px',
                        'top': '120px',
                    });
                    reminder.append(text);
                    main.append(reminder);
                }
            }else if( res.code == 220){
                location.href = '/user/login';
            }else{
                alert(res.data);

            }
        }
    })
})