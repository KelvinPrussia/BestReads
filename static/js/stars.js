document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star-active');
    const selectedRating = document.getElementById('selected-rating');
    const reviewForm = document.getElementById('review-form');
    const alertMessage = document.getElementById('alert-message');

    const initialRating = parseFloat(selectedRating.value);
    highlightStars(initialRating)

    stars.forEach(function (star) {
        star.addEventListener('click', function () {
            const rating = parseFloat(star.getAttribute('data-rating'));
            selectedRating.value = rating;
            highlightStars(rating);
        });

        star.addEventListener('mouseover', function () {
            const rating = parseFloat(star.getAttribute('data-rating'));
            highlightStars(rating);
        });

        star.addEventListener('mouseleave', function () {
            const currentRating = parseFloat(selectedRating.value);
            highlightStars(currentRating);
        });
    });

    reviewForm.addEventListener('submit', function (event) {
        const currentRating = parseFloat(selectedRating.value);
        if (!currentRating) {
            event.preventDefault();
            alertMessage.textContent = 'Please select a star rating.';
            alertMessage.style.display = 'block';
            return false;
        }

        return true;
    })

    function highlightStars(rating) {
        stars.forEach(function (star) {
            const starRating = parseFloat(star.getAttribute('data-rating'));
            if (starRating <= rating) {
                star.style.backgroundImage = "url('static/img/filled-star.png')";
            } else {
                star.style.backgroundImage = "url('static/img/empty-star.png')";
            }
        });
    }
});