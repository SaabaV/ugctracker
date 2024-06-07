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

    $('.status-circle').click(function() {
        var status = $(this).data('status');
        $('.card').each(function() {
            if (status === '' || $(this).data('status') === status) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    class DeleteButton {
        isRunning = false;

        constructor(el) {
            this.el = el;
            this.init();
        }

        init() {
            this.el?.addEventListener("click", this.delete.bind(this));

            const resetTrigger = this.el?.querySelector("[data-anim]");
            resetTrigger?.addEventListener("animationend", this.reset.bind(this));
        }

        delete() {
            this.isRunning = true;
            this.displayState();

            const companyId = this.el.getAttribute('data-company-id');
            const deleteUrl = this.el.getAttribute('data-delete-url');

            if (confirm('Are you sure you want to delete this company from your profile?')) {
                $.ajax({
                    url: deleteUrl,
                    type: 'POST',
                    data: {
                        'company_id': companyId,
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: (response) => {
                        alert('Company deleted successfully');
                        location.reload();
                    },
                    error: (xhr, errmsg, err) => {
                        alert('An error occurred: ' + errmsg);
                        this.reset();
                    }
                });
            } else {
                this.reset();
            }
        }

        displayState() {
            this.el.disabled = this.isRunning;
            this.el.setAttribute("data-running", this.isRunning);
        }

        reset() {
            this.isRunning = false;
            this.displayState();
        }
    }

    document.querySelectorAll('.del-btn').forEach(el => {
        new DeleteButton(el);
    });
});
});
