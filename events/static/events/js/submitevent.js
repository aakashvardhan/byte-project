function myfunc(){
    var frm =$("#formsubmit");
    $.ajax({ 
        type: frm.attr('method'), // GET or POST
        url: frm.attr('action'), // the file to call
        data: frm.serialize(), // get the form data
        success: function () {
        	alert("Event Created!")

        },
        error: function () {
        	alert("Please enter the correct information.")
        }
        });
return false;
}