# YAML Document Overview
Document: `/Users/igor/code/yaml-md/samples/ux/interaction-example.yaml`
Schema: `/Users/igor/code/yaml-md/samples/ux/interaction-ux.schema.yaml`
Objects Indexed: 66

<a id="wf_add_to_cart"></a>
# Workflow: Add Product to Cart

Workflow Id: 
Name: Add Product to Cart
Type: flexible
Application Service: 
State Persistence: 
Strategy: 
Interval: 
Progress Indicator: 
Type: flexible
Position: 

Bounded Contexts: bc_product_catalog bc_shopping_cart

Aggregate Refs: agg_product agg_shopping_cart

## Steps

| Step | Step Id | Page Ref |
| ---- | ------- | -------- |
| View Product Details | select_product | page_product_detail |
| Configure Options | configure_product | page_product_detail |
| Add to Cart | add_to_cart | page_product_detail |

## On Complete: agg_shopping_cart evt_product_added_to_cart page_cart

## Completion: EMPTY → CONTAINS_ITEMS evt_cart_updated toast

| Aggregate Transition | Publishes Event | Navigate To | Feedback |
| -------------------- | --------------- | ----------- | -------- |
| EMPTY → CONTAINS_ITEMS | evt_cart_updated |  | toast |

<a id="wf_user_activation"></a>
# Workflow: User Account Activation

Workflow Id: 
Name: User Account Activation
Type: flexible
Application Service: svc_app_user_management
State Persistence: 
Strategy: 
Interval: 

Bounded Contexts: bc_user_management

Aggregate Refs: agg_user

## Steps

| Step | Step Number | Label | Page Ref | Can Skip | Next Enabled When |
| ---- | ----------- | ----- | -------- | -------- | ----------------- |
| 1 View Pending User page_user_management | 1 | View Pending User | page_user_management | false | user_exists_and_pending |
| 2 Confirm Activation page_user_management | 2 | Confirm Activation | page_user_management | false | validation_passed |

## Validates: on_blur

## Validates: on_submit

## On Complete: agg_user evt_user_activated page_user_management

## Progress Indicator: steps top

| Type | Position |
| ---- | -------- |
| steps | top |

## Completion: PENDING → ACTIVE evt_user_activated page_user_management

| Aggregate Transition | Publishes Event | Navigate To | Feedback |
| -------------------- | --------------- | ----------- | -------- |
| PENDING → ACTIVE | evt_user_activated | page_user_management | toast |

<a id="wf_checkout"></a>
# Workflow: Checkout Process

Workflow Id: 
Name: Checkout Process
Type: linear
Application Service: 
State Persistence: 
Strategy: 
Interval: 

Bounded Contexts: bc_shopping_cart bc_order_management bc_payment

Aggregate Refs: agg_shopping_cart agg_order agg_payment

## Steps

| Step | Step Id | Page Ref | Next Enabled When |
| ---- | ------- | -------- | ----------------- |
| Review Cart | review_cart | page_cart | cart_not_empty |
| Shipping Information | shipping_info | page_checkout_shipping | all_required_fields_valid |
| Payment Information | payment_info | page_checkout_payment | payment_valid |

## On Complete: agg_order evt_order_placed

## Progress Indicator: steps top

| Type | Position |
| ---- | -------- |
| steps | top |

## Completion: PENDING → CONFIRMED evt_order_confirmed page_order_confirmation

| Aggregate Transition | Publishes Event | Navigate To | Feedback |
| -------------------- | --------------- | ----------- | -------- |
| PENDING → CONFIRMED | evt_order_confirmed | page_order_confirmation | modal |