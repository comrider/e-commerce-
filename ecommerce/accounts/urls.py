from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# otp register views
from .views import (
    otp_register,
    otp_sign_in,
    otp_check,
    resent_otp,
    otp_confirm_signup,
    register,
    view_order_,
)

# admin views
from .views import (
    login,
    logout,
    register,
    admin_list_users,
    admin_home,
    admin_user_block,
    admin_user_enable,
    activate,
    admin_list_orders,
    update_order_status,
    view_coupons,
    add_coupon,
    delete_coupon,
    view_variations,
    add_variation,
    delete_variation,
    add_banner,
    delete_banner,
    view_banners,
    # offer
    category_offer,
    add_category_offer,
    delete_category_offer,
    # product offers
    product_offers,
    add_product_offer,
    delete_product_offer,
    # brand offer
    brand_offers,
    add_brand_offer,
    delete_brand_offer,
    ChartData,
    sales_report,
    sales_export_csv,
    sales_export_pdf,
)

# user views
from .views import (
    dashboard,
    forgot_password,
    reset_password,
    my_orders,
    edit_profile,
    change_password,
    cancel_order,
    # cod_payment,
)

urlpatterns = [
    path("sign-up/", otp_register, name="register"),
    path("conform/", otp_confirm_signup, name="confirm"),
    path("otp-sign-in/", otp_sign_in, name="otp_user_login"),
    path("otp-check/", otp_check, name="otp_check"),
    path("resent-otp/", resent_otp, name="resent_otp"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="regular_register"),  # currently hidden from user
    # user
    path("dashboard/", dashboard, name="dashboard"),
    path("my-orders/", my_orders, name="my_orders"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("reset-password/", reset_password, name="reset_password"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("view_order/<str:id>", view_order_, name="view_order_"),
    path("cancel-order/<str:order_number>", cancel_order, name="cancel_order"),
    path("change-password/", change_password, name="change_password"),
    # path("cod-payment/<str:order_number>", cod_payment, name="cod_payment"),
    # admin
    path("admin-login/", login, name="login"),
    path("admin-register/", register, name="admin-register"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path("admin-home/", admin_home, name="admin_home"),
    path("admin-list-users/", admin_list_users, name="admin_list_users"),
    path("admin-disable-users/<int:id>", admin_user_block, name="admin_disable_user"),
    path("admin-enable-users/<int:id>", admin_user_enable, name="admin_enable_user"),
    path("admin-list-orders/", admin_list_orders, name="admin_list_orders"),
    path(
        "order-status-update/<int:order_id>",
        update_order_status,
        name="order_status_update",
    ),
    path("admin-view-coupons/", view_coupons, name="list_coupons"),
    path("admin-add-coupon/", add_coupon, name="add_coupon"),
    path("admin-delete-coupon/<int:coupon_id>/", delete_coupon, name="delete_coupon"),
    path("admin-view-variations/", view_variations, name="view_variations"),
    path("admin-add-variation/", add_variation, name="add_variation"),
    path(
        "admin-delete-variation/<int:variation_id>/",
        delete_variation,
        name="delete_variation",
    ),
    path("admin-add-banner/", add_banner, name="add_banner"),
    path("admin-delete-banner/<int:banner_id>", delete_banner, name="delete_banner"),
    path("admin-view-banners/", view_banners, name="view_banners"),
    # offers
    path("admin-category-offers/", category_offer, name="category_offer"),
    path("admin-add-category-offer/", add_category_offer, name="add_category_offer"),
    path(
        "admin-delete-category-offer/<int:offer_id>/",
        delete_category_offer,
        name="delete_category_offer",
    ),
    path("admin-brand-offers/", brand_offers, name="brand_offers"),
    path("admin-add-brand-offer/", add_brand_offer, name="add_brand_offer"),
    path(
        "admin-delete-brand-offers/<int:offer_id>/",
        delete_brand_offer,
        name="delete_brand_offers",
    ),
    path("admin-product-offers/", product_offers, name="product_offers"),
    path("admin-add-product-offers/", add_product_offer, name="add_product_offers"),
    path(
        "admin-delete-product-offers/<int:offer_id>/",
        delete_product_offer,
        name="delete_product_offers",
    ),
    path("admin-sales-report/", sales_report, name="admin_sales_report"),
    path("api/data/", ChartData.as_view(), name="admin_js_chart"),
    path("admin-sales-report-export-csv/", sales_export_csv, name="sales_export_csv"),
    path("admin-sales-report-export-pdf/", sales_export_pdf, name="sales_export_pdf"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
