// ------- custom js -------- //

//hide initial
$(function() {
    console.log("REaddl");
    console.log(document.cookie);
    $("#convert").click(function() {
        let cookieArray = document.cookie.split(';');
        let data
        console.log(cookieArray);
        for (let i = 0; i < cookieArray.length; i++){
            if (cookieArray[i].search('data') > -1){
                let cookieArrayDetail = cookieArray[i].split('=');
                data = cookieArrayDetail[1];
            }
        }

        let spreadsheet_id = document.getElementById("spreadsheet_id").value;
        let name_sheet = document.getElementById("name_sheet").value;
        let vendor = document.getElementById("vendor").value;
        let tags = document.getElementById("tags").value;

        console.log(name_sheet)
        console.log("readasdasdsa")

        $.ajax({
            type: "POST",
            url: "/convert",
            data: {
                'spreadsheet' : spreadsheet_id,
                'name_sheet':name_sheet,
                'vendor':vendor,
                'tags':tags
            },
            //handle success
            success: function(result) {
                let data = result.results;
                console.log(data)
                for (i = 0; i < data.length; i++) {
                  $("#results").append('<tr><th>'+data[i]["image"]+'</th><th>'+data[i]['score']+'</th></tr>')
                }
            },
             // handle error
            error: function(error) {
                console.log(error);
            }
        });

//        data = data.replaceAll('}', '');
//        data = data.substring(0, data.length-1);
//        console.log(data);
//        let tmp = data.split('{');
//        let name = tmp[1].trim().replaceAll('\\"', '');
//        name = name.substring(0, name.length-1)
//        $("#table_result").show();
//        $("#name_sheet_new").append(name);
//        $("#name_sheet_new").show();
//
//        let mes = tmp[2].split('\\054');
//        for (let i = 0; i < mes.length; i++){
//            mes[i] = mes[i].trim().replaceAll('\\"', '');
//            let temp = mes[i].split(':');
//            console.log(mes[i]);
//            $("#results").append('<tr><th>'+temp[0].trim() + '</th><th>'+temp[1].trim()+'</th></tr>');
//        }
        $("#results").show();

    });


});