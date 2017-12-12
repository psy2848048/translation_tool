var PageScript = function(){
    var local = this;
	this.preInits = function(){
        // body 흐리게
        local.mask();

        // 원문 로딩
        var news_id = getUrlParameter('news_id');
        var jqxhr = $.get( "http://ciceron.xyz:5000/api/v2/mypick/" + news_id, function(data) {
            var html = '';
            $(data.news).each(function(idx, res){
                html += '<tr>';
                html += '    <td>' + res.sentence_id + '</td>';
                html += '    <td>' + res.original + '</td>';
                html += '    <td><textarea rows=1></textarea></td>';
                html += '    <td>';
                html += '        <i class="fa fa-times" aria-hidden="true" style="color:gray; cursor:pointer;"></i>';
                html += '        <i class="fa fa-check" aria-hidden="true" style="color:orange; cursor:pointer; display:none;"></i>';
                html += '    </td>';
                html += '    <td></td>';
                html += '    <td><i class="fa fa-comment" aria-hidden="true" style="color:gray;"></i></td>';
                html += '</tr>';
            });
            $('#mainTbl tbody').append(html);                    
        })
        .done(function() {})
        .fail(function() {alert( "error" );})
        .always(function() {});
        jqxhr.always(function() {
            if($('#mainTbl tbody tr').length < 1) location.href=location.href;
        });
	};
	this.regEvents = function(){      
        // 단어장 검색버튼
        $('#btnPublicSearch').on('click', function(e){
            e.preventDefault();       
            //alert('1. 디비에 저장된 현재 해석문 삭제\n2. 아이콘 체크에서 엑스로 변경');   
            /* 샘플	
            $.ajax({
                url: '/groups/sortGroup',  
                type:'post',
                data:data,
                success:function(args){   
                    alert('ok');
                },   
                error:function(e){  
                    alert('fail');  
                    console.log(e.responseText);  
                }  
            });		
            */            
            var keyword = $('#txtPublicSearch').val();
            alert(keyword + ' 검색(개발중)');

            var result = '<div>';
            result += '    <input type="button" value="저장">';
            result += '    <span class="boldWord">super</span>';
            result += '    <span class="miniWord">1. 대단한, 굉장히 좋은 2. 특별히 3. 경찰서장</span>';
            result += '</div>';

            $('#tran2section table td').prepend(result);
            $('#tran2section table div input[type=button]').on('click', function(e){
                e.preventDefault();
                alert($(this).closest('div').find('.boldWord').text() + ' 저장');
            });
            
        });
        // 원문 클릭
        $('#mainTbl tr td:nth-of-type(2)').on('click', function(e){   
            e.preventDefault();  

            $(document).ajaxStart(function() {
                $('#dvLoading2').show();                         
            });            
            $(document).ajaxComplete(function( event, request, settings ) {
                $('#dvLoading2').hide();
            });
                       
            // 원문 클릭했을 때 (우측에) ajax api 호출, TM, MT 따로 호출해야 함!
            var thisText = $(this).text(), 
                this_idx = $(this).closest('tr').prevAll().length, 
                news_id = getUrlParameter('news_id'), 
                sentence_id = $(this).closest('tr').find('td:eq(0)').text(); // this_idx : 1부터 시작

                console.log('thisText : ' + thisText);                
                console.log('this_idx : ' + this_idx);              
                console.log('news_id : ' + news_id);                
                console.log('sentence_id : ' + sentence_id);      

            $('#resultTbl').html('');

            // TM
            local.getTmAjax(news_id, sentence_id, thisText, this_idx);

            // MT
            local.getMtAjax(thisText, this_idx);

            // TB
            local.getTBAjax();
        });
        // 선택된 해석문 textarea 클릭
        // keyup 으로 하면 로딩부터 실행 주의!
        $('#mainTbl textarea').on('keyup', function(e){
            e.preventDefault();         
            //alert('1. 디비에 저장된 현재 해석문 삭제\n2. 아이콘 체크에서 엑스로 변경');   
            /* 샘플	
            $.ajax({
                url: '/groups/sortGroup',  
                type:'post',
                data:data,
                success:function(args){   
                    alert('ok');
                },   
                error:function(e){  
                    alert('fail');  
                    console.log(e.responseText);  
                }  
            });		
            */            
            $(this).closest('tr').find('td:eq(3)').find('.fa-check').hide();
            $(this).closest('tr').find('td:eq(3)').find('.fa-times').show();
        });
        // x 버튼 클릭
        $('.fa-times').on('click', function(e){
            e.preventDefault();
            // 현재의 해석문 저장하고 아이콘 변경
            //alert('1. 현재의 번역참고문 디비에 저장\n2. 아이콘 완료(체크)로 변경');
            /* 샘플	
            $.ajax({
                url: '/groups/sortGroup',  
                type:'post',
                data:data,
                success:function(args){   
                    alert('ok');
                },   
                error:function(e){  
                    alert('fail');  
                    console.log(e.responseText);  
                }  
            });		
            */     
            $(this).hide();
            $(this).next().show();
        });
        // 체크 버튼 클릭
        $('.fa-check').on('click', function(e){
            e.preventDefault();
            //alert('1. 현재의 해석문 디비에서 삭제\n2. 아이콘 미완료(x)로 초기화');
            // 현재의 해석문 삭제하고 아이콘 변경
            /* 샘플	
            $.ajax({
                url: '/groups/sortGroup',  
                type:'post',
                data:data,
                success:function(args){   
                    alert('ok');
                },   
                error:function(e){  
                    alert('fail');  
                    console.log(e.responseText);  
                }  
            });		
            */     
            $(this).hide();
            $(this).prev().show();
        });
        // 탭1
        $('#tabTbl td:nth-of-type(1)').on('click', function(e){
            e.preventDefault();
            $('#resultTbl').show();
            $('#resultTbl2').hide();
            $('#tabTbl td:nth-of-type(1)').css({'font-weight':'bold','border':'1px solid rgba(207, 204, 204, 0.404)', 'border-top':'0px', 'border-left':'0px', 'background-color':'rgb(252, 253, 252)'});
            $('#tabTbl td:nth-of-type(2)').css({'border':'1px solid rgba(207, 204, 204, 0.404)', 'border-right':'0px', 'border-bottom':'0px', 'font-weight':'normal', 'background-color':'#fff'});            
            $('#tran1section').show();
            $('#tran2section').show();
        });
        // 탭2
        $('#tabTbl td:nth-of-type(2)').on('click', function(e){
            e.preventDefault();
            $('#resultArea').css({'border-top':'0'});
            $('#resultTbl').hide();
            $('#resultTbl2').show();
            $('#tabTbl td:nth-of-type(1)').css({'font-weight':'normal', 'border-bottom':'0px', 'border-left':'0px', 'border-top':'1px solid rgba(207, 204, 204, 0.404)', 'background-color':'#fff'});            
            $('#tabTbl td:nth-of-type(2)').css({'font-weight':'bold', 'border':'1px solid rgba(207, 204, 204, 0.404)', 'border-top':'0px', 'border-right':'0px', 'background-color':'rgb(252, 253, 252)'});            
            $('#tran1section').hide();
            $('#tran2section').hide();
        });

        // 완전히 로딩 후 로더 숨김
        $('#dvLoading').hide();    
            
        // 마스크 해제       
        //애니메이션 효과 - 일단 1초동안 초기화 됐다가 0% 불투명도로 변화.
        $('#mask').fadeIn(1000);      
        $('#mask').fadeTo("slow",1000).hide();    
    };
    this.textAreaExpand = function(){
        $('#mainTbl').on( 'keyup', 'textarea', function (e){
            e.preventDefault();            
            $(this).css('height', 'auto' );
            $(this).height( this.scrollHeight );
        });
        //$('#mainTbl').find( 'textarea' ).keyup();
    },
    this.mask = function(){
        //화면의 높이와 너비를 구한다.
        var maskHeight = $(document).height();  
        var maskWidth = $(window).width();  
        
        //마스크의 높이와 너비를 화면 것으로 만들어 전체 화면을 채운다.
        $('#mask').css({'width':maskWidth,'height':maskHeight});  
    };   
    this.getTmAjax = function(news_id, sentence_id, thisText, this_idx){
        var jqxhr = $.get( "http://ciceron.xyz:5000/api/v2/mypick/" + news_id + "/" + sentence_id , function(data) {
            console.log('result1');
            console.log(data);
            
            var tm_html = '<tr>';
            tm_html += '    <td width="4%" style="text-align:center;">1</td>';
            tm_html += '    <td width="45%">' + thisText + ' </td>';
            tm_html += '    <td width="5%" class="tmColor" style="text-align:center;">TM</td>';                       
            tm_html += '    <td width="46%">' + data.translated + '</td>';
            tm_html += '</tr>';

            $('#resultArea').css({'border-top':'0'});
            $('#resultTbl').append(tm_html);  
            // 이벤트 등록
            $('#resultTbl tr').on('click', function(e){
                e.preventDefault();
                //alert('1. 좌측에 해석문 입력\n2. 아이콘 x 로 변경 혹은 유지\n3. TM/TB/MT 선택에 따른 변경');
                var transType = $(this).find('td:eq(2)').text();
                var transBgClass = '';
                switch (transType) {
                    case 'TM' : transBgClass = 'tmColor'; break;
                    case 'TB' : transBgClass = 'tbColor'; break;
                    case 'MT' : transBgClass = 'mtColor'; break;
                    default :; break;
                }
                $('#mainTbl tr:nth-of-type(' + parseInt(this_idx+1) + ') td:nth-of-type(3) textarea').val($(this).find('td:nth-of-type(4)').text()).keyup();
                $('#mainTbl tr:nth-of-type(' + parseInt(this_idx+1) + ') td:nth-of-type(4) i:nth-of-type(2)').hide();
                $('#mainTbl tr:nth-of-type(' + parseInt(this_idx+1) + ') td:nth-of-type(4) i:nth-of-type(1)').show();
                $('#mainTbl tr:nth-of-type(' + parseInt(this_idx+1) + ') td:nth-of-type(5)').removeClass().addClass(transBgClass).html(transType);
            });                
        })
        .done(function() {
        })
        .fail(function() {
            alert( "error" );
        })
        .always(function() {});
        jqxhr.always(function() {});  
    };
    this.getMtAjax = function(thisText, this_idx){
        var data = {
            "source_lang_id":2, // 1: 한국어 2: 영어
            "target_lang_id":1,  // 1: 한국어 2: 영어
            "where":"phone", // 노상관
            "sentence": thisText, // 번역할문장
            "user_email":"admin@sexycookie.com" // 일종의 암호로, 이거 바꾸면 안돌아가요
        };
        $.ajax({
            url: 'http://52.196.164.64/translate',  
            type:'post',
            data:data,
            async:true, 
            success:function(args){  
                console.log('result2');
                console.log(args);
                var mt_html = '<tr>';
                mt_html += '    <td width="4%" style="text-align:center;">2</td>';
                mt_html += '    <td width="45%">' + thisText + ' </td>';
                mt_html += '    <td width="5%" class="mtColor" style="tsext-align:center;">MT</td>';                      
                mt_html += '    <td width="46%">' + args.google + '</td>';
                mt_html += '</tr>';   
                
                $('#resultArea').css({'border-top':'0'});
                $('#resultTbl').append(mt_html);  
                // 이벤트 등록
                $('#resultTbl tr').on('click', function(e){
                    e.preventDefault();
                    //alert('1. 좌측에 해석문 입력\n2. 아이콘 x 로 변경 혹은 유지\n3. TM/TB/MT 선택에 따른 변경');
                    var transType = $(this).find('td:eq(2)').text();
                    var transBgClass = '';
                    switch (transType) {
                        case 'TM' : transBgClass = 'tmColor'; break;
                        case 'TB' : transBgClass = 'tbColor'; break;
                        case 'MT' : transBgClass = 'mtColor'; break;
                        default :; break;
                    }
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx+1) + ') td:nth-of-type(3) textarea').val($(this).find('td:nth-of-type(4)').text()).keyup();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx+1) + ') td:nth-of-type(4) i:nth-of-type(2)').hide();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx+1) + ') td:nth-of-type(4) i:nth-of-type(1)').show();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx+1) + ') td:nth-of-type(5)').removeClass().addClass(transBgClass).html(transType);
                });                                 
            },   
            error:function(e){  
                alert('fail');  
                console.log(e.responseText);  
            }  
        });
        this.getTBAjax = function(){
            $('#tran2section table td').empty();
            
            var result = '';       
            //alert('1. 디비에 저장된 현재 해석문 삭제\n2. 아이콘 체크에서 엑스로 변경');   
            /* 샘플	
            $.ajax({
                url: '/groups/sortGroup',  
                type:'post',
                data:data,
                success:function(args){   
                    alert('ok');
                },   
                error:function(e){  
                    alert('fail');  
                    console.log(e.responseText);  
                }  
            });		
            */            
            result += '<div>';
            result += '<input type="button" value="저장"> ';
            result += '<span class="boldWord">book</span> ';
            result += '<span class="miniWord">1. 책 2. (종이・전자 형태의) 저서, 도서, 책 3. (글을 쓸 수 있게 책 모양으로 엮은) 종이 묶음</span>';
            result += '</div>';

            result += '<div>';
            result += '    <input type="button" value="저장"> ';
            result += '    <span class="boldWord">apple</span> ';
            result += '    <span class="miniWord">사과</span> ';
            result += '</div>';

            $('#tran2section table td').append(result);

            $('#tran2section table div input[type=button]').on('click', function(e){
                e.preventDefault();
                alert($(this).closest('div').find('.boldWord').text() + ' 저장');
            });
        };
    };
	this.bind = function(){
        local.preInits();
	};
};
$(function(){
	var script = new PageScript();
    script.bind();

    setTimeout(function(){        
        script.regEvents();	
        script.textAreaExpand();	
        $('#mainTbl tr').show();
    }, 3000);    
});
