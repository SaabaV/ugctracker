$(document).ready(function() {
    $('#edit-profile-btn').click(function() {
        $('#edit-profile-form').toggleClass('hidden');
    });

    $('#profile-edit-form').on('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: "/user_profile/edit_profile/",
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.avatar_url) {
                    $('.user-avatar').attr('src', response.avatar_url);
                }
                $('#display-goal').text(response.goal);
                $('#display-date-of-birth').text(response.date_of_birth);
                $('#edit-profile-form').addClass('hidden');
            },
            error: function(response) {
                console.log('Error:', response);
            }
        });
    });

   $('.toggle-info').off('click').on('click', function(event) {
        event.stopPropagation();
        event.preventDefault();

        var additionalInfo = $(this).siblings('.additional-info');
        if (additionalInfo.is(':visible')) {
            additionalInfo.slideDown();
            $(this).text('Show less');
        } else {
            additionalInfo.slideUp();
            $(this).text('Show more');
        }
    });

    // Обработчик для кнопки редактирования компании
    $('.edit-company').click(function() {
        var companyId = $(this).data('company-id');
        $('#edit-form-' + companyId).toggle();
    });

    $(document).ready(function () {
    $('.edit-company').click(function () {
        var companyId = $(this).data('company-id');
        $('#edit-form-' + companyId).toggle();
    });

    $('.delete-company').click(function (e) {
        e.preventDefault();
        var companyId = $(this).data('company-id');
        var deleteUrl = $(this).data('delete-url');
        if (confirm('Are you sure you want to delete this company from your profile?')) {
            $.ajax({
                url: deleteUrl,
                type: 'POST',
                data: {
                    'company_id': companyId,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function (response) {
                    alert('Company deleted successfully');
                    location.reload();
                },
                error: function (xhr, errmsg, err) {
                    alert('An error occurred: ' + errmsg);
                }
            });
        }
    });
});
});

