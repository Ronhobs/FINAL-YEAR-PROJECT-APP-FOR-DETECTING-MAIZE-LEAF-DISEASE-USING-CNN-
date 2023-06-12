$(document).ready(function () {
    // Initialization
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#btn-predict').show(); // Make predict button visible

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    // Event listener for file upload input
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict button click handler
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling API /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text('Result: ' + data);
                console.log('Success!');
            },
        });
    });
});
