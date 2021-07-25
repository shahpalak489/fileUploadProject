$(document).ready(function() {
    function readfile(file) {
        $(".file-name").html('');
        const fileName = file.files[0].name;
        $(".file-name").append("File Name: ".concat(fileName));
        $(".file-name").css('display', 'block');
        $(".submit-btn").css('display', 'block');
    }
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/uploader',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data, status, xhr) {
                $.ajax({
                    type: 'GET',
                    url: 'fetch',
                    contentType: 'application/json',
                    dataType: 'json',
                    success: function(data, status, xhr) {
                        console.log(data.data)
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
                            html += "<td>" + value.share_price + "</td>";
                            html += "<td>" + value.share_price_dt + "</td>";
                            html += "<td>" + value.comments + "</td>";
                            html += "</tr>";
                        });
                        $('#company-detail-data').html(html);
                        // window.location.href = 'file_upload';
                    },
                });
            },
        });
    });
    getCompanyList();
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
                console.log('Error in company fetch!');
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
            },
            error: function(data, status, xhr) {
                console.log('Error in company add!');
            }
        });
    });
});
