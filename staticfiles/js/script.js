$(document).ready(function() {
    // Autocomplete search
    $('#movieSearch').on('input', function() {
        const query = $(this).val();
        if (query.length > 2) {
            $.ajax({
                url: '/autocomplete/',
                data: { 'term': query },
                success: function(data) {
                    let suggestions = '';
                    data.forEach(movie => {
                        suggestions += `<div class="suggestion-item" data-title="${movie}">${movie}</div>`;
                    });
                    $('#suggestions').html(suggestions).show();
                }
            });
        } else {
            $('#suggestions').hide();
        }
    });

    // Suggestion selection
    $(document).on('click', '.suggestion-item', function() {
        $('#movieSearch').val($(this).data('title'));
        $('#suggestions').hide();
    });

// Theme toggle
$('#themeToggle').click(function() {
    $('body').toggleClass('dark-theme light-theme');
    const icon = $(this).find('i');
    const button = $(this);
    
    if ($('body').hasClass('light-theme')) {
        icon.removeClass('fa-moon').addClass('fa-sun');
        button.removeClass('btn-outline-primary').addClass('btn-outline-secondary');
    } else {
        icon.removeClass('fa-sun').addClass('fa-moon');
        button.removeClass('btn-outline-secondary').addClass('btn-outline-primary');
    }
    
    // Save theme preference
    const theme = $('body').hasClass('light-theme') ? 'light' : 'dark';
    localStorage.setItem('theme', theme);
});

// Load saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    $('body').addClass('light-theme').removeClass('dark-theme');
    $('#themeToggle i').removeClass('fa-moon').addClass('fa-sun');
    $('#themeToggle').removeClass('btn-outline-primary').addClass('btn-outline-secondary');
}

    // Popular movie badges
    $('.badge.pointer').click(function() {
        $('#movieSearch').val($(this).text());
        $('#suggestions').hide();
    });
});