function SetPagebar(total_count, row_size, cur_page, org_url, pagebar_size) {
    if (parseInt(total_count) > 0) {
        var total_page_count = parseInt(((total_count - 1) / row_size) + 1);

        var start_page = parseInt((cur_page - 1) / pagebar_size) * pagebar_size + 1; // 정수로 계산되어야 하기에 반드시 parseInt() 해줘야 한다!!
        
        var end_page;
        if ((start_page + pagebar_size - 1) < total_page_count) {
            end_page = start_page + pagebar_size - 1;
        } else {
            end_page = total_page_count;
        }

        var html = '';

        if (cur_page != '1') html += '<li><a href="' + org_url + 'page=1"><i class="fa fa-arrow-circle-left" aria-hidden="true"></i> 첫 페이지</a></li>';
        else html += '<li style="opacity:0.3;cursor:auto;"><i class="fa fa-arrow-circle-left" aria-hidden="true"></i> 첫 페이지</li>';

        if (parseInt((cur_page - 1) / pagebar_size) > 0) html += '    <li><a href="' + org_url + 'page=' + parseInt(start_page - pagebar_size) + '"><i class="fa fa-arrow-circle-o-left" aria-hidden="true"></i> 이전 10 페이지</a></li>';
        else html += '    <li style="opacity:0.3;cursor:auto;"><i class="fa fa-arrow-circle-o-left" aria-hidden="true"></i> 이전 10 페이지</li>';

        for (var i = start_page; i <= end_page; i++) {
            if (i == cur_page) html += '        <li style="background-color:rgb(214, 216, 81);"><a href="' + org_url + 'page=' + i + '">' + i + '</a></li>';
            else html += '        <li><a href="' + org_url + 'page=' + i + '">' + i + '</a></li>';
        }

        if (end_page < total_page_count) html += '    <li><a href="' + org_url + 'page=' + parseInt(end_page + 1) + '">다음 10 페이지 <i class="fa fa-arrow-circle-o-right" aria-hidden="true"></i></a></li>';
        else html += '    <li style="opacity:0.3;cursor:auto;">다음 10 페이지 <i class="fa fa-arrow-circle-o-right" aria-hidden="true"></i></li>';

        if (cur_page != total_page_count) html += '<li><a href="' + org_url + 'page=' + total_page_count + '">마지막 페이지 <i class="fa fa-arrow-circle-right" aria-hidden="true"></i></a></li>';
        else html += '<li style="opacity:0.3;cursor:auto;">마지막 페이지 <i class="fa fa-arrow-circle-right" aria-hidden="true"></i></li>';

        $('#page_bar ul').html('<br>' + html);
    }
}
// 임시호출 : 각 페이지마다 커스텀하게 별도로 호출해줘야 함!!
SetPagebar(2500, 15, getUrlParameter('page') == undefined || getUrlParameter('page') == '' ? 1 : getUrlParameter('page'), $(location).attr('pathname') + '?', 10);