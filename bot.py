services = {
    "Catering": {"Basic": 15000, "Standard": 25000, "Premium": 40000},
    "Decoration": {"Basic": 8000, "Standard": 15000, "Premium": 25000},
    "Photography": {"Basic": 10000, "Standard": 20000, "Premium": 30000},
    "Venue": {"Basic": 20000, "Standard": 30000, "Premium": 50000},
    "Entertainment": {"Basic": 5000, "Standard": 10000, "Premium": 15000}
}

print("🎉 Welcome to the AI-like Event Cost Estimation & Negotiation Bot 🎉")
print("\nAvailable Services & Tiers:")
for service, tiers in services.items():
    print(f"\n{service}:")
    for tier, price in tiers.items():
        print(f"  {tier} - ₹{price}")

selected_services = {}
while True:
    service = input("\nEnter a service (or type 'done' to finish): ").strip().title()
    if service.lower() == 'done':
        break
    if service in services:
        print(f"Available Tiers for {service}: {list(services[service].keys())}")
        tier = input(f"Choose tier for {service} (Basic / Standard / Premium): ").strip().title()
        if tier in services[service]:
            selected_services[service] = tier
        else:
            print("❌ Invalid tier. Try again.")
    else:
        print("❌ Invalid service. Try again.")

if not selected_services:
    print("⚠️ No services selected. Exiting.")
    exit()


total_cost = sum(services[s][t] for s, t in selected_services.items())
print(f"\n💰 Estimated Total Cost: ₹{total_cost}")


try:
    budget = int(input("Enter your budget: ₹"))
except ValueError:
    print("❌ Invalid input. Please enter a numeric value.")
    exit()

removed_services = []
final_cost = total_cost


optional_services = ["Entertainment", "Photography", "Decoration"]
if budget < final_cost:
    print("\n🤖 Budget too low. Checking for optional services to remove...")
    for service in optional_services:
        if service in selected_services and final_cost > budget:
            final_cost -= services[service][selected_services[service]]
            removed_services.append(service)
            print(f"⚠️ Removed optional service: {service}")


if budget < final_cost:
    gap = final_cost - budget
    discount_percent = min(0.2, gap / final_cost)  
    discount_amount = min(int(final_cost * discount_percent), final_cost)
    final_cost = max(final_cost - discount_amount, 0)
else:
    discount_amount = 0


print("\n📣 Bot Reasoning Summary:")
if budget >= total_cost:
    print("- Budget sufficient. No changes needed.")
else:
    print(f"- Initial Total Cost: ₹{total_cost}")
    if removed_services:
        print(f"- Removed optional services: {', '.join(removed_services)}")
    if discount_amount > 0:
        print(f"- Applied discount of ₹{discount_amount} ({int((discount_amount / total_cost) * 100)}%)")
    print(f"- Final offer matched to your budget 🎯")


print("\n-----------------------------")
print("🧾 FINAL INVOICE")
print("-----------------------------")
print("Service        | Tier     | Price (₹)")
print("-----------------------------")
services_displayed = False
final_services_cost = 0
for service, tier in selected_services.items():
    if service not in removed_services:
        price = services[service][tier]
        print(f"{service:<14} {tier:<9} ₹{price}")
        final_services_cost += price
        services_displayed = True

if not services_displayed:
    print("⚠️ All services were removed. No billable items.")
print("-----------------------------")
print(f"Original Cost            ₹{total_cost}")
if discount_amount > 0:
    print(f"Discount Applied         ₹{discount_amount}")
if removed_services:
    print(f"Services Removed         {', '.join(removed_services)}")
print(f"Final Negotiated Cost    ₹{final_cost}")
print("-----------------------------")


with open("event_invoice.txt", "w", encoding="utf-8") as f:
    f.write("🧾 Event Invoice\n")
    f.write("-----------------------------\n")
    for service, tier in selected_services.items():
        if service not in removed_services:
            price = services[service][tier]
            f.write(f"{service} ({tier}): ₹{price}\n")
    f.write("-----------------------------\n")
    f.write(f"Original Cost: ₹{total_cost}\n")
    if discount_amount > 0:
        f.write(f"Discount Applied: ₹{discount_amount}\n")
    if removed_services:
        f.write(f"Services Removed: {', '.join(removed_services)}\n")
    f.write(f"Final Cost: ₹{final_cost}\n")

print("✅ Invoice saved as 'event_invoice.txt'")