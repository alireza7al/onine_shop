    document.querySelector('.add-to-cart').addEventListener('click', function() {
        this.classList.add('added');
        setTimeout(() => {
            this.classList.remove('added');
        }, 1000);
    });

    document.querySelector('.read-more').addEventListener('click', function() {
        const description = document.querySelector('.description');
        description.classList.toggle('expanded');
        this.textContent = description.classList.contains('expanded') ? 'کمتر بخوانید' : 'بیشتر بخوانید';
    });

