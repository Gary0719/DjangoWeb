$(function(){
    var token = window.localStorage.getItem('community_token');
    var username = window.localStorage.getItem('community_user');
    var myhead = window.localStorage.getItem('head_portrait');
    var friendhead = $("#friend img").attr('src');
    var friend = $("#friend span").html();
    $.ajax({
        url:'/letter/record/'+username+'/with/'+friend,
        type:'get',
        dataType:'json',
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", token);
        },
        success:function(res){
            if(res.code == 200){
                record = $('<div id="record"></div>');
                $("#show_letter").prepend(record);
                for(var i=0;i<res.data.length;i++){
                    content = res.data[i];
                    r = $('<div id="record'+(i+1)+'"></div>').css({
                        'position': 'relative',
                        'width': '800px',
                        'height': '40px',
                        // 'border': '1px solid #666',
                    });
                    l = $('<span class="letter">'+content.letter+'</span>').css({
                        'display': 'inline-block',
                        'font-size': '16px',
                        'color': '#fff',
                        'border-radius': '3px',
                        'background-color': 'rgba(0, 0, 0, 0.5)',
                        'padding': '0 8px',
                        'position': 'absolute',
                        'top': '10px',
                    });
                    if(content.sender == username){
                        l.css({
                            'right': '50px'
                        });
                        h = $('<img src="" alt="">').attr('src',myhead).css({
                            'width': '36px',
                            'height': '36px',
                            'border-radius': '50%',
                            'position': 'absolute',
                            'right': '5px',
                            'top': '2px',
                        });
                    }else{
                        l.css({
                            'left': '50px'
                        });
                        h = $('<img src="" alt="">').attr('src',friendhead).css({
                            'width': '36px',
                            'height': '36px',
                            'border-radius': '50%',
                            'position': 'absolute',
                            'left': '5px',
                            'top': '2px',
                        });
                    }
                    // t = $('<div class="time">'+content.time.substring(0,19)+'</div>').css({
                    //     'position': 'absolute',
                    //     'left': '350px',
                    //     'color': '#fff',
                    //     'border-radius': '3px',
                    //     'background-color': 'rgba(0, 0, 0, 0.5)',
                    //     'font-size': '12px',
                    // });
                    
                    r.prepend(l);
                    l.after(h);
                    record.before(r);
                };
            }else if(res.code == 281){
                alert(res.data);
            }
        }
    })

    $("#my button").click(function(){
        var letter = $("#my_letter").val();
        var friend = $("#friend span").html();
        // console.log(letter,friend);
        $.ajax({
            url:'/letter/'+username+'/with/'+friend,
            type:'post',
            dataType:'json',
            contentType:'application/json;charset:utf-8',
            data:JSON.stringify({
                'letter':letter,
            }),
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success:function(res){
                if(res.code == 200){
                    location.reload();
                }else if(res.code == 220){
                    alert(res.data);
                }else if(res.code == 276){
                    alert(res.data);
                }else if(res.code == 277){
                    alert(res.data);
                }else if(res.code == 278){
                    alert(res.data);
                }
            }
        })
    })
})