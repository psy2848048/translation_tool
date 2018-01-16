var pageScript = function () {
    var local = this,
        rows = IsValidStr(getUrlParameter('rows')) ? getUrlParameter('rows') : '15',
        page = IsValidStr(getUrlParameter('page')) ? getUrlParameter('page') : '1',
        cur_path = $(location).attr('pathname');
    this.preInits = function () {
        local.showList();
    };
    this.keyupEvents = function () {
        $(document).on('keyup', '#listTitleGroup textarea', function (e) {
            e.preventDefault();
            $(this).css('height', 'auto');
            $(this).height(this.scrollHeight);
        });
        //$('#listTitleGroup').find('textarea').keyup();
    };
    this.outFocusEvents = function(){
        $(document).on('focusout', '#listTitleGroup table td input[type=text], #listTitleGroup table td textarea', function(e){
            e.preventDefault();
            var thisTr = $(this).closest('tr');
            var data = {
                origin_lang:thisTr.find('td:eq(1) input[type=text]').val(),
                origin_text:thisTr.find('td:eq(2) textarea').val(),
                trans_lang:thisTr.find('td:eq(3) input[type=text]').val(),
                trans_text:thisTr.find('td:eq(4) textarea').val()
            };
            console.log('[data] : ', data);
            $.ajax({
                url: '/api/v1/toolkit/transMemory/' + thisTr.find('td:eq(0)').text(),
                type: 'PUT',
                data: data,
                async: true,
                success: function (args) {
                    if(args.result == 'OK'){
                        //alert('정상적으로 저장되었습니다.');
                        //location.href='project_view.html?project=' + project_id;
                    }else{
                        alert('저장에 실패했습니다.\n\n오류코드 : 6456');
                    }
                },
                error: function (err) {
                    alert('fail : error code 2154');
                    console.log('fail : error code 2154');
                    console.log(err.responseText);
                }
            });
        });
    };
    this.clickEvents = function () {
        $('#new_li_btn').on('click', function (e) {
            e.preventDefault();
            local.showPopup();
        });
        $(document).on('click', '#listTitleGroup table td .fa-times', function (e) {
            e.preventDefault();
            var id = $(this).closest('tr').find('td:eq(0)').text();
            $.ajax({
                url: '/api/v1/toolkit/transMemory/' + id,
                type: 'DELETE',
                async: true,
                success: function (res) {
                    console.log('[5462 res] : ', res);
                    if (res.result == 'OK') {
                        alert('문장이 삭제되었습니다.');
                        location.href = location.href;
                        //local.showList();
                    }
                },
                error: function (e) {
                    console.log('fail 6653');
                    console.log(e.responseText);
                }
            });
        });
        $('#upload_div .fa-times').on('click', function (e) {
            e.preventDefault();
            $('#upload_div').hide();
            $('#mainWrap').css('opacity', '1');
        });
    };
    this.selectEvent = function () {
        $('#file_upload_frm').on('change', function (e) {
            e.preventDefault();
            //var reg_ext = ['JPG','JPEG','GIF','PNG'];
            var reg_ext = ['CSV'];
            var msg = 'CSV 파일 확장자만 허용합니다.';
            onFileSelect($('#file_upload_frm'), '/api/v1/toolkit/transMemory/', 5, reg_ext, msg);
        });
    };
    this.show = function () {
        //화면의 높이와 너비를 구한다.
        var maskHeight = $(document).height();  
        var maskWidth = $(window).width();  
        
        //마스크의 높이와 너비를 화면 것으로 만들어 전체 화면을 채운다.
        $('#mask').css({'width':maskWidth,'height':maskHeight}); 
    };
    this.hide = function(){
        //$('#mask').fadeIn(1000);      
        $('#mask').fadeTo("slow", 1000).hide();    
        $('#loading_img').fadeTo("slow", 1000).hide();    
    };
    this.showList = function () {
        local.show();
        var list = $.get('/api/v1/toolkit/transMemory?rows=' + rows + '&page=' + page, function (data) {
                console.log('/api/v1/toolkit/transMemory?rows=' + rows + '&page=' + page, data);
                if (data != undefined && data != null && data.results != undefined && data.results != null && parseInt(data.results.length) > 0) {
                    var row = '';
                    $(data.results).each(function (idx, res) {
                        row += '<tr>';
                        row += '    <td>' + res.tmid + '</td>';
                        row += '    <td>';
                        row += '        <input type="text" value="' + res.origin_lang + '">';
                        row += '    </td>';
                        row += '    <td>';
                        row += '        <textarea rows="1">' + res.origin_text + '</textarea>';
                        row += '    </td>';
                        row += '    <td>';
                        row += '        <input type="text" value="' + res.trans_lang + '">';
                        row += '    </td>';
                        row += '    <td>';
                        row += '        <textarea rows="1">' + res.trans_text + '</textarea>';
                        row += '        ';
                        row += '    </td>';
                        row += '    <td>';
                        row += '        <i class="fa fa-times" aria-hidden="true"></i>';
                        row += '    </td>';
                        row += '</tr>';
                    });
                    $('#listTitleGroup table tbody').append(row);
                    $('#listTitleGroup textarea').keyup();
                }
                var param_path = cur_path + '?rows=' + rows + '&';
                SetPagebar(parseInt(data.total_cnt), rows, page, param_path, 10);
            })
            .done(function () {})
            .fail(function () {
                console.log("error 3396");
            })
            .always(function () {});
        list.always(function () {
            local.hide();
        });
    };
    this.showPopup = function () {
        $('#mainWrap').css('opacity', '0.2');
        $("#upload_div").show();
        $("#upload_div").center();
    };
    this.bind = function () {
        local.preInits();
        local.outFocusEvents();
        local.keyupEvents();
        local.clickEvents();
        local.selectEvent();
    };
};
$(function () {
    var script = new pageScript();
    script.bind();
});