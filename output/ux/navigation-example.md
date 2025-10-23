# YAML Document Overview
Document: `/Users/igor/code/yaml-md/samples/ux/navigation-example.yaml`
Schema: `/Users/igor/code/yaml-md/samples/ux/navigation-ux.schema.yaml`
Objects Indexed: 48

# Navigation

## Local Navigation

| Local Navigation | Scope | Scope Id | Pattern |
| ---------------- | ----- | -------- | ------- |
| [Localnav Product Detail](#localnav_product_detail) | page | page_product_detail | tabs |

## Global Navigation: top_horizontal top true

Pattern: top_horizontal
Position: top
Sticky: true

### Items

| Item | Label | Target | Icon | Bounded Context |
| ---- | ----- | ------ | ---- | --------------- |
| [Home](#nav_home) | Home | page_home | home |  |
| [Products](#nav_products) | Products | page_category_list |  | bc_product_catalog |
| [Deals](#nav_deals) | Deals | page_deals |  | bc_promotions |
| [Cart](#nav_cart) | Cart | page_cart | shopping-cart | bc_shopping_cart |
| [Account](#nav_account) | Account | page_account | user | bc_customer_account |

### Badge: count active_deals_count

### Badge: count cart_items_count

## Utility Navigation

### User Menu: avatar

Trigger: avatar

Items:
- Label: My Orders Target: page_orders
- Label: Wishlist Target: page_wishlist
- Label: Settings Target: page_settings
- Label: Sign Out Target: /auth/signout

### Search: header Cmd+K

| Position | Shortcut |
| -------- | -------- |
| header | Cmd+K |

### Notifications: header unread_notifications_count

| Position | Badge Source |
| -------- | ------------ |
| header | unread_notifications_count |

## Mobile Navigation: bottom_tabs 768

| Pattern | Breakpoint |
| ------- | ---------- |
| bottom_tabs | 768 |