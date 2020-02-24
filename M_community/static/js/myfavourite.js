$(function(){
    var token = window.localStorage.getItem('community_token');
    var username = window.localStorage.getItem('community_user');
    $.ajax({
        url: '/essay/my_favourite_data',
        type: 'get',
        dataType: 'json',
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", token);
        },
        success: function(res){
            if (res.code == 200){
                main = $("#main");
                for (var i=0; i < res.data.length; i++){
                    one = $('<div class="one_favourite"></div>').css({
                        'width': '330px',
                        'height': '400px',
                        'float': 'left',
                        'border': '2px solid #666',
                        'border-radius': '10px',
                        'margin-top': '10px',
                        'margin-left': '8px',
                        'margin-right': '8px',
                        'margin-bottom': '20px',
                        'position': 'relative',
                    });
                    essay_id = $('<span class="essay_id"></span>').html(res.data[i].essay_id).css({
                        'display': 'none',
                    });
                    essay_title = $('<span class="essay_title"></span>').html(res.data[i].title).css({
                        'display': 'inline-block',
                        'width': '300px',
                        'font-size': '16px',
                        'font-weight': '900',
                        'position': 'absolute',
                        'left': '20px',
                        'top': '10px',
                    });
                    essay_classify = $('<span class="essay_classify"></span>').html('分类:' + res.data[i].classify).css({
                        'display': 'inline-block',
                        'font-size': '15px',
                        'position': 'absolute',
                        'left': '25px',
                        'top': '55px',
                        'background-color': 'rgba(0, 0, 0, 0.3)',
                        'padding-left': '5px',
                        'padding-right': '5px',
                        'border-radius': '5px',
                        'color': '#fff',
                    });
                    essay_click = $('<span class="essay_click"></span>').html('点击率:' + res.data[i].click_rate).css({
                        'display': 'inline-block',
                        'font-size': '15px',
                        'position': 'absolute',
                        'left': '110px',
                        'top': '55px',
                        'color': '#c20c0b',
                    });
                    essay_image = $('<img src="" class="essay_image">').attr('src', res.data[i].image).css({
                        'width': '300px',
                        'height': '225px',
                        'position': 'absolute',
                        'left': '15px',
                        'bottom': '90px',
                        'border-radius': '10px',
                        'cursor': 'pointer',
                    });
                    author_name = $('<span class="author_name"></span>').html(res.data[i].author_name).css({
                        'display': 'inline-block',
                        'width': '210px',
                        'position': 'absolute',
                        'left': '25px',
                        'bottom': '55px',
                        'font-size': '15px',
                        'font-weight': '900',
                        'color': '#4080e2',
                    });
                    author_gender = $('<span class="author_gender"></span>').html(res.data[i].author_gender).css({
                        'font-size': '15px',
                        'position': 'absolute',
                        'left': '25px',
                        'bottom': '30px',
                    });
                    author_head = $('<img src=""  class="author_image">').attr('src', res.data[i].author_head).css({
                        'width': '70px',
                        'height': '70px',
                        'border-radius': '10px',
                        'position': 'absolute',
                        'right': '15px',
                        'bottom': '10px',
                    });
                    one.append(essay_id)
                    one.append(essay_title);
                    one.append(essay_classify);
                    one.append(essay_click);
                    one.append(essay_image);
                    one.append(author_name);
                    one.append(author_gender);
                    one.append(author_head);
                    main.append(one);


                    essay_image.click(function(){
                        essay_id = $(this).siblings('.essay_id').html();
                        author = $(this).siblings('.author_name').html();
                        location.href = '/essay/detail/' + author + '/' + essay_id;
                    })
                };
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
                    text = $('<span>收藏夹里空空如也呢~</span>').css({
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
                
            }else{
                // alert(res.data);
                location.href = '/user/login';
            }
        }
    })
})