// تابع برای پرداخت
document.getElementById("checkout-btn").addEventListener("click", () => {
    // ارسال درخواست به سرور برای خالی کردن سبد خرید
    fetch("/checkout/", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            // به‌روزرسانی صفحه پس از پرداخت
            location.reload();
        })
        .catch(error => {
            console.error("خطا در پرداخت:", error); // فقط خطا را در کنسول نمایش دهید
        });
});