# SFPS Customer Command Centre

## Scope
Corporate workspaces and role-based access; order history, tracking, partial shipments, ETA and delivery requests; RFQs, quotations, BOM and PO uploads; Zoho Books organisation 948681972 invoices, statements, credit notes and approved credit terms; payment links; account-specific pricing and framework agreements; warranty, RMA and technical support; Fyber Optix compatibility and catalogue links; staff administration and audit history; Resend notifications.

## Release gates
- Authenticate and authorize every company-scoped request; test cross-tenant denial.
- Store uploads privately with size/type validation, malware scanning and authorized downloads.
- Verify Shopify and Zoho identity mapping, webhook signatures, replay protection and idempotency.
- Verify finance data against Zoho; never display invented balances or discounts.
- Test tracking creation, update, lookup and unauthorized access.
- Test mobile UI and navigation; preserve existing supplier portal.
- Publish customer-facing Shopify navigation only after acceptance tests pass.

## Commercial rules
Discount tiers and credit limits are proposals only until individually approved; no automatic financial commitments.

## Navigation
Portals > Customer Portal, Track My Order, Apply for a Trade Account, Supplier Portal, Technical Support.
