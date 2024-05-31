$(document).ready(function() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('.add-to-my-company').click(function() {
        var companyId = $(this).data('company-id');
        console.log('Company ID:', companyId);  // Добавим логирование
        var csrftoken = getCookie('csrftoken');
        console.log('CSRF Token:', csrftoken);  // Добавим логирование

        $.ajax({
            url: "/add_to_my_company/",
            type: 'POST',
            data: {
                'company_id': companyId,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                if (response.message) {
                    alert(response.message);
                } else if (response.error) {
                    alert('Error: ' + response.error);
                }
            },
            error: function(response) {
                alert('Error: ' + response.responseText);
            }
        });
    });
    
    $('.edit-company').click(function() {
        var companyId = $(this).data('company-id');
        $('#edit-form-' + companyId).toggle();
    });
    $('.edit-company-form').submit(function(event) {
            event.preventDefault();
            var form = $(this);
            var formData = form.serialize();
            var csrftoken = getCookie('csrftoken');
            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                data: formData,
                success: function(response) {
                    if (response.success) {
                        alert('Company updated successfully');
                        location.reload();
                    } else {
                        alert('Failed to update the company');
                    }
                },
                error: function(xhr, status, error) {
                    alert('Error: ' + xhr.responseText);
                }
            });
        });
    });

    $('#avatar-container').on('click', function () {
        document.getElementById('avatar-input').click();
    });

    $('#avatar-input').on('change', function () {
        document.getElementById('avatar-form').submit();
    });

    $('#avatar-form').on('submit', function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.new_avatar_url) {
                    $('#avatar-container img').attr('src', response.new_avatar_url + '?' + new Date().getTime());
                    location.reload();
                }
            },
            error: function (xhr, status, error) {
                alert('Error uploading avatar: ' + xhr.responseText);
            }
        });
    });

    $('#add-company-form').on('submit', function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                window.location.reload();
                $('.card').slice(-3).addClass('animated fadeInUp');
            },
            error: function (xhr, status, error) {
                alert('Error adding company: ' + xhr.responseText);
            }
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
        function checkFields() {
            const fields = [
                { id: 'company.deal_amount', hrId: 'hr-deal-amount' },
                { id: 'company.content_count', hrId: 'hr-content-count' }
            ];
            fields.forEach(field => {
                const fieldElement = document.querySelector(`[data-field="${field.id}"]`);
                const hrElement = document.getElementById(field.hrId);
                if (fieldElement && fieldElement.textContent.trim() !== '') {
                    hrElement.classList.remove('hidden');
                } else {
                    hrElement.classList.add('hidden');
                }
            });
        }

        checkFields();
    });

    document.querySelectorAll('.toggle-info').forEach(button => {
        button.addEventListener('click', function () {
            let additionalInfo = this.parentElement.querySelector('.additional-info');
            if (additionalInfo.style.display === "none" || additionalInfo.style.display === "") {
                additionalInfo.style.display = "block";
                this.textContent = "Show less";
            } else {
                additionalInfo.style.display = "none";
                this.textContent = "Show more";
            }
        });
    });

    $('#save-goal-btn').click(function (e) {
        e.preventDefault();
        var goal = $('#goal-select').val();
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: "/user_profile/save_goal/",
            type: 'POST',
            data: {
                'goal': goal,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function (response) {
                $('#display-goal').text(response.goal);
                alert('Goal updated successfully');
            },
            error: function (response) {
                console.log('Error:', response);
            }
        });
    });












