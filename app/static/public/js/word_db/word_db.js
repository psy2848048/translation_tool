var pageScript = function () {
    var local = this,
        rows = IsValidStr(getUrlParameter('rows')) ? getUrlParameter('rows') : '15',
        page = IsValidStr(getUrlParameter('page')) ? getUrlParameter('page') : '1',
        cur_path = $(location).attr('pathname'),
        lang = IsValidStr(getUrlParameter('lang')) ? getUrlParameter('lang') : '1',
        o_lang, t_lang;
    this.preInits = function () {
        $('#search_box select').val(lang);
        local.showList();

        jQuery.fn.center = function () {
            this.css("position", "absolute");
            this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2 - 100) + $(window).scrollTop()) +
                "px");
            this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + $(window).scrollLeft()) +
                "px");
            return this;
        };
    };
    this.outFocusEvents = function () {
        $(document).on('focusout', '#listTitleGroup table td input[type=text]', function (e) {
            e.preventDefault();
            var thisTr = $(this).closest('tr');
            var data = {
                origin_lang: thisTr.find('td:eq(1) input[type=text]').val(),
                origin_text: thisTr.find('td:eq(2) input[type=text]').val(),
                trans_lang: thisTr.find('td:eq(3) input[type=text]').val(),
                trans_text: thisTr.find('td:eq(4) input[type=text]').val()
            };
            console.log('[data] : ', data);
            $.ajax({
                url: '/api/v1/toolkit/termbase/' + thisTr.find('td:eq(0)').text(),
                type: 'PUT',
                data: data,
                async: true,
                success: function (args) {
                    if (args.result == 'OK') {
                        //alert('정상적으로 저장되었습니다.');
                        //location.href='project_view.html?project=' + project_id;
                    } else {
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
    this.showPopup = function () {
        $('#mainWrap').css('opacity', '0.2');
        $("#upload_div").show();
        $("#upload_div").center();
    };
    this.keyupEvents = function () {
        $(document).on('keyup', '#listTitleGroup textarea', function (e) {
            e.preventDefault();
            $(this).css('height', 'auto');
            $(this).height(this.scrollHeight);
        });
        $('#listTitleGroup').find('textarea').keyup();
    };
    this.clickEvents = function () {
        $('#search_box input').on('click', function (e) {
            e.preventDefault();
            local.getSelectedLang();
            location.href='/static/front/word_db/word_db.html?rows=' + rows + '&lang=' + $('#search_box select').val();
        });
        $('#new_li_btn').on('click', function (e) {
            e.preventDefault();
            local.showPopup();
        });
        $(document).on('click', '#listTitleGroup table td .fa-times', function (e) {
            e.preventDefault();
            if (confirm('정말로 삭제하시겠습니까?')) {
                var id = $(this).closest('tr').find('td:eq(0)').text();
                $.ajax({
                    url: '/api/v1/toolkit/termbase/' + id,
                    type: 'DELETE',
                    async: true,
                    success: function (res) {
                        console.log('[5462 res] : ', res);
                        if (res.result == 'OK') {
                            alert('단어가 삭제되었습니다.');
                            location.href = location.href;
                            //local.showList();
                        }
                    },
                    error: function (e) {
                        console.log('fail 6653');
                        console.log(e.responseText);
                    }
                });
            }
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
            onFileSelect($('#file_upload_frm'), '/api/v1/toolkit/termbase/', 5, reg_ext, msg, 'upload_result');
        });
    };
    this.show = function () {
        //화면의 높이와 너비를 구한다.
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();

        //마스크의 높이와 너비를 화면 것으로 만들어 전체 화면을 채운다.
        $('#mask').css({
            'width': maskWidth,
            'height': maskHeight
        });
    };
    this.hide = function () {
        //$('#mask').fadeIn(1000);      
        $('#mask').fadeTo("slow", 1000).hide();
        $('#loading_img').fadeTo("slow", 1000).hide();
    };
    this.getSelectedLang = function () {
        switch ($('#search_box select').val()) {
            case '1':
                local.o_lang = 'EN';
                local.t_lang = 'KO';
                break;
            case '2':
                local.o_lang = 'EN';
                local.t_lang = 'ZH';
                break;
            case '3':
                local.o_lang = 'ZH';
                local.t_lang = 'KO';
                break;
            case '4':
                local.o_lang = 'ZH';
                local.t_lang = 'EN';
                break;
            case '5':
                local.o_lang = 'KO';
                local.t_lang = 'EN';
                break;
            case '6':
                local.o_lang = 'KO';
                local.t_lang = 'ZH';
                break;
        }
    };
    this.showList = function () {
        local.getSelectedLang();
        local.show();

        var list = $.get('/api/v1/toolkit/termbase?origin_lang=' + local.o_lang + '&trans_lang=' + local.t_lang + '&rows=' + rows + '&page=' + page, function (data) {
                var row = '';
                row += '<tr>';
                row += '    <th>#</th>';
                row += '    <th colspan="2">단어</th>';
                row += '    <th colspan="2">해석</th>';
                row += '    <th>';
                row += '        <i class="fa fa-times" aria-hidden="true"></i>';
                row += '    </th>';
                row += '</tr>';
                console.log('/api/v1/toolkit/termbase?origin_lang=' + local.o_lang + '&trans_lang=' + local.t_lang + '&rows=' + rows + '&page=' + page);
                console.log(data);
            if (data != undefined && data != null && data.results != undefined && data.results != null && parseInt(data.results.length) > 0) {
                    $(data.results).each(function (idx, res) {
                        row += '<tr>';
                        row += '    <td>' + res.tid + '</td>';
                        row += '    <td>';
                        row += '        <input type="text" value="' + res.origin_lang + '">';
                        row += '    </td>';
                        row += '    <td>';
                        row += '        <input type="text" value="' + res.origin_text + '">';
                        row += '    </td>';
                        row += '    <td>';
                        row += '        <input type="text" value="' + res.trans_lang + '">';
                        row += '    </td>';
                        row += '    <td>';
                        row += '        <input type="text" value="' + res.trans_text + '">';
                        row += '        ';
                        row += '    </td>';
                        row += '    <td>';
                        row += '        <i class="fa fa-times" aria-hidden="true"></i>';
                        row += '    </td>';
                        row += '</tr>';
                    });
                }
                $('#listTitleGroup table').html(row);
                $('#listTitleGroup textarea').keyup();
                var param_path = cur_path + '?lang=' + $('#search_box select').val() + '&rows=' + rows + '&';
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