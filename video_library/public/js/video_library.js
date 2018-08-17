$(document).ready(function () {
    window.full_name = getCookie("full_name");
    var logged_in = getCookie("sid") && getCookie("sid") !== "Guest";
    if (window.location.pathname == '/premium-videos') {
        console.log(logged_in)
        if (logged_in == false) {
            
            frappe.msgprint("<b>Please purchase premium plan</b>", 'Access Denied')
            window.setTimeout(function () {
                window.location = "/";
            }, 2000);
        } else {
            var user_role
            frappe.call({
                method: 'video_library.api.get_website_user_role',
                args: {
                    username: frappe.session.user
                },
                callback: function (r) {
                    console.log(r.message)
                    user_role = r.message
                    if ($("div:contains('Please sign-up or login to begin')").length == 10 || user_role != 'premiumuser') {
                        frappe.msgprint("<b>Please purchase premium plans</b>", 'Access Denied')
                        window.setTimeout(function () {
                            window.location = "/basic-videos";
                        }, 2000);
                    }
                }
            })
        }
    }
    if (window.location.pathname == '/basic-videos' && logged_in == false) {
        frappe.msgprint("<b>Please purchase basic plan</b>", 'Access Denied')
        window.setTimeout(function () {
            window.location = "/";
        }, 2000);

    }
});