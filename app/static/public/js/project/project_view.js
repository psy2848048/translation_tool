var PageScript = function(){
    var local = this,
        project_id = getUrlParameter('project');
	this.preInits = function(){                   
        // body 흐리게
        local.mask();    

        // 임시alert(project_id);
        if(project_id == 2){ // 중문번역
            $('#dvTitle h2').text('내픽뉴스 중문번역');
            $('#tblProjectDetail tr:nth-of-type(1) td:nth-of-type(2)').text('2');
            $('#tblProjectDetail tr:nth-of-type(1) td:nth-of-type(4)').html('ZH<span class="super">CN</span>');
            $('#tblProjectDetail tr:nth-of-type(2) td:nth-of-type(2)').text('내픽뉴스 중문번역');
        }
    };
	this.btnEvents = function(){   
    
    };
    this.getProjects = function(){
        var url = project_id == '1' ? 'http://ciceron.xyz:5000/api/v2/mypick/en' : 'http://ciceron.xyz:5000/api/v2/mypick/cn';
        
        if(project_id == '1') $('#menuArea ul li ul li:nth-of-type(1) a').css({'color':'orange'});
        else $('#menuArea ul li ul li:nth-of-type(2) a').css({'color':'orange'});

        $(document).ajaxStart(function() {
            $('#dvLoading').show();                         
        });            
        $(document).ajaxComplete(function( event, request, settings ) {
            $('#dvLoading').hide();
        });

        var jqxhr = $.get(url , function(data) {
            console.log(data);  
            var row = '';
            $(data.news).each(function(idx, res){
                row += '<tr>';
                row += '    <td><input type="checkbox"></td>';
                row += '    <td>' + parseInt(idx+1) + '</td>';
                row += '    <td>60%</td>';
                row += '    <td style="width:calc(100%);text-align:left;vertical-align:middle;" class="oneline_wrap"><a target="_blank" href="../trans/trans.html?news_id=' + res.id + '">' + res.name + '</a></td>';
                row += '    <td>신규</td>';
                row += '    <td><a target="_blank" href="http://ciceron.me/translated/38/45">링크</a></td>';
                row += '    <td>KO<span class="super">KR</span></td>';
                row += '    <td>김 철수</td>';
                row += '    <td>2018-02-21 10:11</td>';
                row += '</tr>';
            });
            $('#listContents table tbody').append(row);                                
        })
        .done(function() {
        })
        .fail(function() {
            alert( "error" );
        })
        .always(function() {});
        jqxhr.always(function() {});  

        $('#mask').fadeIn(1000);      
        $('#mask').fadeTo("slow",1000).hide();    
    };
    this.mask = function(){
        //화면의 높이와 너비를 구한다.
        var maskHeight = $(document).height();  
        var maskWidth = $(window).width();  
        
        //마스크의 높이와 너비를 화면 것으로 만들어 전체 화면을 채운다.
        $('#mask').css({'width':maskWidth,'height':maskHeight});  
    };
    this.bind = function(){
        local.preInits();
        local.btnEvents();
        local.getProjects(getUrlParameter('project'));
    };
};
$(function(){
    var script = new PageScript();
    script.bind();
});