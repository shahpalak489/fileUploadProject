$(document).ready(function() {
    getCompanyList();

    function formatDate(date) {
        var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();
        if (month.length < 2) 
            month = '0' + month;
        if (day.length < 2) 
            day = '0' + day;
        return [year, month, day].join('-');
    }

    function toast(message, status) {
        $(".toast").css("display", "flex");
        $(".toast-text").text(message);
        if (status){
            $(".fas").removeClass("fa-times error")
            $(".fas").addClass("fa-check success")
            $(".toast").css("background-color", "green");
        } else {
            $(".fas").removeClass("fa-check success")
            $(".fas").addClass("fa-times error")
            $(".toast").css( "background-color", "red");
        }
        setTimeout(function () {
            $(".toast").css("display", "none");
        }, 3000);
    }

    $("#file-upload").click(function(e){
        e.target.value = null
    });

    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/file/uploader',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data, status, xhr) {
                $("#detail-data-block").css("display","flex")
                toast(data.data, data.success);
                $.ajax({
                    type: 'GET',
                    url: 'fetch/uploaded/companies/v1',
                    contentType: 'application/json',
                    dataType: 'json',
                    success: function(data, status, xhr) {
                        let html = "";
                        html += "<tr>";
                        html += "<th class='table-header upload-content'>" + 'Company Id' + "</th>";
                        html += "<th class='table-header upload-content'>" + 'Company Name' + "</th>";
                        html += "<th class='table-header upload-content'>" + 'Share price' + "</th>";
                        html += "<th class='table-header upload-content'>" + 'share price date' + "</th>";
                        html += "<th class='table-header upload-content'>" + 'Comments' + "</th>";
                        html += "</tr>";
                        $.each(data.data, function (key, value) {
                            html += "<tr>";
                            html += "<td>" + value.cid + "</td>";
                            html += "<td>" + value.cname + "</td>";
                            html += "<td>" + '$' + value.share_price + "</td>";
                            html += "<td>" + formatDate(value.share_price_dt) + "</td>";
                            html += "<td>" + value.comments + "</td>";
                            html += "</tr>";
                        });
                        $('#company-detail-data').html(html);
                    },
                    error: function(data, status, xhr) {
                        toast(xhr, true);
                    }
                });
            },
        });
    });

    function getCompanyList() {
        $.ajax({
            type: 'GET',
            url: 'company/list/v1',
            contentType: 'application/json',
            dataType: 'json',
            success: function(data, status, xhr) {
                let html = "";
                html += "<tr>";
                html += "<th class='table-header upload-content'>" + 'Company Id' + "</th>";
                html += "<th class='table-header upload-content'>" + 'Company Name' + "</th>";
                html += "</tr>";
                $.each(data.data, function (key, value) {
                    html += "<tr>";
                    html += "<td>" + value.cid + "</td>";
                    html += "<td>" + value.cname + "</td>";
                    html += "</tr>";
                });
                $('#company-list').html(html);
            },
            error: function(data, status, xhr) {
                toast(xhr, true);
            }
        });
    }

    $('#add_company').click(function() {
        const c_id = $("#company-id" ).val();
        const c_name = $("#company-name" ).val();
        const data = { c_id, c_name }
        $.ajax({
            type: 'PUT',
            url: '/company/list/v1',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({"data": data}),
            success: function(data, status, xhr) {
                $("#company-id" ).val('');
                $("#company-name" ).val('');
                getCompanyList();
                toast(data.data, data.success);
            },
            error: function(data, status, xhr) {
                toast(xhr, true);
            }
        });
    });
});
