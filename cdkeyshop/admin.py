from django.contrib import admin
from .models import Category, Product, ProductsCategories, Order, OrderProduct, TrendingProduct


class ProductsCategoriesInline(admin.TabularInline):
    model = ProductsCategories


class OrderProductInline(admin.TabularInline):
    model = OrderProduct


class TrendingProductInline(admin.TabularInline):
    model = TrendingProduct


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductsCategoriesInline,
        TrendingProductInline,
    ]


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductsCategoriesInline,
    ]


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderProductInline,
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(TrendingProduct)
