"use client";
import Button from "@/components/button";
import Modal from "@/components/modal";
import React, { useState, useEffect } from "react";
import {
  createOrder,
  getAllOrders,
  Order,
  OrderCreateData,
  OrderItem,
} from "@/lib/api/services/orderServices";
import {
  createProduct,
  getAllProducts,
  Product,
  ProductCreateData,
} from "@/lib/api/services/productServices";
import {
  createPayment,
  getAllPayments,
  Payment,
  PaymentCreateData,
} from "@/lib/api/services/paymentServices";
import {
  createCustomer,
  getAllCustomers,
  Customer,
  CustomerCreateData,
} from "@/lib/api/services/customerServices";
import { toast } from "react-toastify";
import { useMutation, useQuery } from "@tanstack/react-query";
import { getAllUsers } from "@/lib/api/services/userServices";

const DataHuntPage = () => {
  console.log("🎬 DataHuntPage component rendering");

  // Modal states
  const [isOrdersOpen, setIsOrdersOpen] = useState(false);
  const [isPaymentsOpen, setIsPaymentsOpen] = useState(false);
  const [isProductsOpen, setIsProductsOpen] = useState(false);
  const [isUsersOpen, setIsUsersOpen] = useState(false);
  const [isCustomerOpen, setIsCustomerOpen] = useState(false);
  const [isCreateOrderOpen, setIsCreateOrderOpen] = useState(false);
  const [isCreatePaymentOpen, setIsCreatePaymentOpen] = useState(false);
  const [isCreateProductOpen, setIsCreateProductOpen] = useState(false);
  const [isCreateUserOpen, setIsCreateUserOpen] = useState(false);
  const [isCreateCustomerOpen, setIsCreateCustomerOpen] = useState(false);

  const generateRandomName = () => {
    const firstNames = [
      "Amit",
      "Pooja",
      "Rahul",
      "Anjali",
      "Vikas",
      "Shivani",
      "Rakesh",
      "Neha",
      "Sanjay",
      "Priya",
      "Arjun",
      "Kavita",
      "Manoj",
      "Ritu",
      "Deepak",
      "Suman",
    ];
    const lastNames = [
      "Yadav",
      "Singh",
      "Verma",
      "Sharma",
      "Gupta",
      "Mishra",
      "Pandey",
      "Khan",
      "Chauhan",
      "Patel",
      "Tiwari",
      "Maurya",
      "Srivastava",
      "Rathore",
    ];
    return `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${
      lastNames[Math.floor(Math.random() * lastNames.length)]
    }`;
  };

  const generateRandomDate = (startYear: number, endYear: number) => {
    const start = new Date(startYear, 0, 1);
    const end = new Date(endYear, 11, 31);
    const randomDate = new Date(
      start.getTime() + Math.random() * (end.getTime() - start.getTime())
    );
    return randomDate.toISOString().split("T")[0];
  };
  // Data states
  const [orders, setOrders] = useState<Order[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(false);

  // Form states
  const [orderForm, setOrderForm] = useState<OrderCreateData>({
    customer_id: "",
    customer_name: "",
    customer_email: "",
    customer_phone: "",
    items: [],
    shipping_address: {
      street: "",
      city: "",
      state: "",
      zip_code: "",
      country: "",
    },
    payment_method: "credit_card",
    notes: "",
  });

  const [productForm, setProductForm] = useState<ProductCreateData>({
    name: "",
    description: "",
    sku: "",
    category: "",
    brand: "",
    price: 0,
    stock_quantity: 0,
    is_active: true,
  });

  const [paymentForm, setPaymentForm] = useState<PaymentCreateData>({
    order_id: "",
    customer_id: "",
    amount: 0,
    currency: "USD",
    payment_method: "credit_card",
    payment_provider: "stripe",
    transaction_type: "purchase",
  });

  const [customerForm, setCustomerForm] = useState<CustomerCreateData>({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    address_line1: "",
    address_line2: "",
    city: "",
    state: "",
    postal_code: "",
    country: "",
    date_of_birth: "",
    gender: "prefer_not_to_say",
    company_name: "",
    tax_id: "",
    marketing_emails: true,
    marketing_sms: false,
    notes: "",
    tags: "",
  });

  const {
    data: customersRes,
    isLoading: isCustomersLoading,
    refetch: refetchCustomers,
  } = useQuery({
    queryKey: ["customers"],
    queryFn: () => getAllCustomers(),
  });
  const {
    data: ordersRes,
    isLoading: isOrdersLoading,
    refetch: refetchOrders,
  } = useQuery({
    queryKey: ["orders"],
    queryFn: () => getAllOrders(),
  });
  const {
    data: productsRes,
    isLoading: isProductsLoading,
    refetch: refetchProducts,
  } = useQuery({
    queryKey: ["products"],
    queryFn: () => getAllProducts(),
  });
  const {
    data: paymentsRes,
    isLoading: isPaymentsLoading,
    refetch: refetchPayments,
  } = useQuery({
    queryKey: ["payments"],
    queryFn: () => getAllPayments(),
  });
  const {
    data: usersRes,
    isLoading: isUsersLoading,
    refetch: refetchUsers,
  } = useQuery({
    queryKey: ["users"],
    queryFn: () => getAllUsers(),
  });
  console.log("customersRes", customersRes);
  console.log("ordersRes", ordersRes);
  console.log("productsRes", productsRes);
  console.log("paymentsRes", paymentsRes);
  console.log("usersRes", usersRes);
  // Modal handlers
  const handleOrdersModal = () => setIsOrdersOpen(!isOrdersOpen);
  const handlePaymentsModal = () => setIsPaymentsOpen(!isPaymentsOpen);
  const handleProductsModal = () => setIsProductsOpen(!isProductsOpen);
  const handleUsersModal = () => setIsUsersOpen(!isUsersOpen);
  const handleCustomerModal = () => setIsCustomerOpen(!isCustomerOpen);
  const handleCreateOrderModal = () => setIsCreateOrderOpen(!isCreateOrderOpen);
  const handleCreateProductModal = () =>
    setIsCreateProductOpen(!isCreateProductOpen);
  const handleCreatePaymentModal = () =>
    setIsCreatePaymentOpen(!isCreatePaymentOpen);
  const handleCreateCustomerModal = () =>
    setIsCreateCustomerOpen(!isCreateCustomerOpen);

  // Form handlers
  const handleOrderFormChange = (field: keyof OrderCreateData, value: any) => {
    setOrderForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleProductFormChange = (
    field: keyof ProductCreateData,
    value: any
  ) => {
    setProductForm((prev) => ({ ...prev, [field]: value }));
  };

  const handlePaymentFormChange = (
    field: keyof PaymentCreateData,
    value: any
  ) => {
    setPaymentForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleCustomerFormChange = (
    field: keyof CustomerCreateData,
    value: any
  ) => {
    setCustomerForm((prev) => ({ ...prev, [field]: value }));
  };

  // Submit handlers
  const handleCreateOrder = async () => {
    try {
      setLoading(true);
      await createOrder(orderForm);
      toast.success("Order created successfully!");
      handleCreateOrderModal();
      setOrderForm({
        customer_id: "",
        customer_name: "",
        customer_email: "",
        customer_phone: "",
        items: [],
        shipping_address: {
          street: "",
          city: "",
          state: "",
          zip_code: "",
          country: "",
        },
        payment_method: "credit_card",
        notes: "",
      });
    } catch (error) {
      console.error("Error creating order:", error);
      toast.error("Failed to create order");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProduct = async () => {
    try {
      setLoading(true);
      await createProduct(productForm);
      toast.success("Product created successfully!");
      handleCreateProductModal();
      setProductForm({
        name: "",
        description: "",
        sku: "",
        category: "",
        brand: "",
        price: 0,
        stock_quantity: 0,
        is_active: true,
      });
    } catch (error) {
      console.error("Error creating product:", error);
      toast.error("Failed to create product");
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePayment = async () => {
    try {
      setLoading(true);
      await createPayment(paymentForm);
      toast.success("Payment created successfully!");
      handleCreatePaymentModal();
      setPaymentForm({
        order_id: "",
        customer_id: "",
        amount: 0,
        currency: "USD",
        payment_method: "credit_card",
        payment_provider: "stripe",
        transaction_type: "purchase",
      });
    } catch (error) {
      console.error("Error creating payment:", error);
      toast.error("Failed to create payment");
    } finally {
      setLoading(false);
    }
  };
  const { mutate: createCustomerMutation } = useMutation({
    mutationFn: (customer: CustomerCreateData) => createCustomer(customer),
    onSuccess: () => {
      refetchCustomers();
      toast.success("Customer created successfully!");
    },
    onError: () => {
      toast.error("Failed to create customer");
    },
  });
  const handleCreateCustomer = async () => {
    try {
      setLoading(true);
      createCustomerMutation(customerForm);
      handleCreateCustomerModal();
      setCustomerForm({
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        address_line1: "",
        address_line2: "",
        city: "",
        state: "",
        postal_code: "",
        country: "",
        date_of_birth: "",
        gender: "prefer_not_to_say",
        company_name: "",
        tax_id: "",
        marketing_emails: true,
        marketing_sms: false,
        notes: "",
        tags: "",
      });
    } catch (error) {
      console.error("Error creating customer:", error);
      toast.error("Failed to create customer");
    } finally {
      setLoading(false);
    }
  };

  const addOrderItem = () => {
    const newItem: OrderItem = {
      product_id: "",
      product_name: "",
      quantity: 1,
      unit_price: 0,
      subtotal: 0,
    };
    setOrderForm((prev) => ({
      ...prev,
      items: [...prev.items, newItem],
    }));
  };

  const updateOrderItem = (
    index: number,
    field: keyof OrderItem,
    value: any
  ) => {
    setOrderForm((prev) => ({
      ...prev,
      items: prev.items.map((item, i) =>
        i === index ? { ...item, [field]: value } : item
      ),
    }));
  };

  const removeOrderItem = (index: number) => {
    setOrderForm((prev) => ({
      ...prev,
      items: prev.items.filter((_, i) => i !== index),
    }));
  };

  // Generate dummy data functions
  const generateOrderData = () => {
    const dummyOrder: OrderCreateData = {
      customer_id: `CUST_${Math.random()
        .toString(36)
        .substr(2, 8)
        .toUpperCase()}`,
      customer_name: "John Doe",
      customer_email: "john.doe@example.com",
      customer_phone: "+1-555-0123",
      items: [
        {
          product_id: "PROD_001",
          product_name: "Laptop Computer",
          quantity: 1,
          unit_price: 1299.99,
          subtotal: 1299.99,
        },
        {
          product_id: "PROD_002",
          product_name: "Wireless Mouse",
          quantity: 2,
          unit_price: 29.99,
          subtotal: 59.98,
        },
      ],
      shipping_address: {
        street: "123 Main Street",
        city: "New York",
        state: "NY",
        zip_code: "10001",
        country: "USA",
      },
      payment_method: "credit_card",
      notes: "Please deliver during business hours",
    };
    setOrderForm(dummyOrder);
  };

  const generateProductData = () => {
    const dummyProduct: ProductCreateData = {
      name: "Smartphone X Pro",
      description:
        "Latest smartphone with advanced features, high-resolution camera, and long battery life",
      sku: `SKU_${Math.random().toString(36).substr(2, 6).toUpperCase()}`,
      category: "Electronics",
      brand: "TechCorp",
      price: 899.99,
      sale_price: 799.99,
      cost_price: 450.0,
      stock_quantity: 50,
      min_stock_level: 10,
      weight: 0.18,
      dimensions: {
        length: 15.5,
        width: 7.5,
        height: 0.8,
      },
      images: [
        {
          url: "https://example.com/images/smartphone-x-pro-1.jpg",
          alt_text: "Smartphone X Pro Front View",
          is_primary: true,
        },
      ],
      variants: [
        {
          name: "Color",
          value: "Midnight Black",
          price_adjustment: 0,
        },
        {
          name: "Storage",
          value: "128GB",
          price_adjustment: 0,
        },
      ],
      specifications: [
        {
          name: "Screen Size",
          value: "6.1 inches",
          unit: "inches",
        },
        {
          name: "Battery Capacity",
          value: "4000",
          unit: "mAh",
        },
      ],
      tags: ["smartphone", "5G", "camera", "battery"],
      is_featured: true,
      is_active: true,
      meta_title: "Smartphone X Pro - Latest Technology",
      meta_description:
        "Experience the future with Smartphone X Pro featuring cutting-edge technology",
    };
    setProductForm(dummyProduct);
  };

  const generatePaymentData = () => {
    const dummyPayment: PaymentCreateData = {
      order_id: `ORD_${Math.random().toString(36).substr(2, 8).toUpperCase()}`,
      customer_id: `CUST_${Math.random()
        .toString(36)
        .substr(2, 8)
        .toUpperCase()}`,
      amount: 1359.97,
      currency: "USD",
      payment_method: "credit_card",
      payment_provider: "stripe",
      transaction_type: "purchase",
      description: "Payment for electronics order",
      metadata: {
        source: "web",
        campaign: "summer_sale_2024",
      },
      payment_method_details: {
        card_last4: "4242",
        card_brand: "visa",
        card_exp_month: 12,
        card_exp_year: 2026,
      },
    };
    setPaymentForm(dummyPayment);
  };

  const generateCustomerData = () => {
    const dummyCustomer: CustomerCreateData = {
      first_name: generateRandomName().split(" ")[0],
      last_name: generateRandomName().split(" ")[1] || "Smith",
      email: `customer${Math.random().toString(36).substr(2, 6)}@example.com`,
      phone: `+1-555-${Math.random().toString().substr(2, 3)}-${Math.random()
        .toString()
        .substr(2, 4)}`,
      address_line1: `${Math.floor(Math.random() * 9999) + 1} ${
        ["Main St", "Oak Ave", "Pine Rd", "Elm Blvd"][
          Math.floor(Math.random() * 4)
        ]
      }`,
      address_line2:
        Math.random() > 0.5 ? `Apt ${Math.floor(Math.random() * 999) + 1}` : "",
      city: [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
      ][Math.floor(Math.random() * 8)],
      state: ["NY", "CA", "IL", "TX", "AZ", "PA", "FL", "OH"][
        Math.floor(Math.random() * 8)
      ],
      postal_code: Math.floor(Math.random() * 99999 + 10000).toString(),
      country: "USA",
      date_of_birth: generateRandomDate(1980, 2000),
      gender: ["male", "female", "other", "prefer_not_to_say"][
        Math.floor(Math.random() * 4)
      ] as "male" | "female" | "other" | "prefer_not_to_say",
      company_name:
        Math.random() > 0.3
          ? `Company ${Math.random().toString(36).substr(2, 6).toUpperCase()}`
          : "",
      tax_id:
        Math.random() > 0.5
          ? `TAX-${Math.random().toString(36).substr(2, 8).toUpperCase()}`
          : "",
      marketing_emails: Math.random() > 0.3,
      marketing_sms: Math.random() > 0.7,
      notes: Math.random() > 0.5 ? "Sample customer for testing purposes" : "",
      tags: ["sample", "test", "dummy"].join(", "),
    };
    setCustomerForm(dummyCustomer);
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Data Hunt</h1>
      <p className="text-gray-600 mb-6">
        Data Hunt is a platform for finding and analyzing data.
      </p>

      <div className="grid grid-cols-3 gap-6">
        {/* Orders Section */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Orders</h3>
          <div className="grid grid-cols-2 gap-3">
            <Button
              onClick={handleCreateOrderModal}
              variant="primary"
              size="md"
            >
              Create Order
            </Button>
            <Button onClick={handleOrdersModal} variant="secondary" size="md">
              View Orders ({orders.length})
            </Button>
            <Button
              onClick={() => refetchOrders()}
              variant="secondary"
              size="md"
            >
              refetch
            </Button>
          </div>
        </div>

        {/* Payments Section */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Payments</h3>
          <div className="grid grid-cols-2 gap-3">
            <Button
              onClick={handleCreatePaymentModal}
              variant="primary"
              size="md"
            >
              Create Payment
            </Button>
            <Button onClick={handlePaymentsModal} variant="secondary" size="md">
              View Payments ({payments.length})
            </Button>
            <Button
              onClick={() => refetchPayments()}
              variant="secondary"
              size="md"
            >
              refetch
            </Button>
          </div>
        </div>

        {/* Products Section */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Products</h3>
          <div className="grid grid-cols-2 gap-3">
            <Button
              onClick={handleCreateProductModal}
              variant="primary"
              size="md"
            >
              Create Product
            </Button>
            <Button onClick={handleProductsModal} variant="secondary" size="md">
              View Products ({products.length})
            </Button>
            <Button
              onClick={() => refetchProducts()}
              variant="secondary"
              size="md"
            >
              refetch
            </Button>
          </div>
        </div>

        {/* Users Section */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Users</h3>
          <div className="grid grid-cols-2 gap-3">
            <Button onClick={() => {}} variant="primary" size="md">
              Create User
            </Button>
            <Button onClick={handleUsersModal} variant="secondary" size="md">
              View Users
            </Button>
            <Button
              onClick={() => refetchUsers()}
              variant="secondary"
              size="md"
            >
              refetch
            </Button>
          </div>
        </div>

        {/* Customers Section */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Customers</h3>
          <div className="grid grid-cols-2 gap-3">
            <Button
              onClick={handleCreateCustomerModal}
              variant="primary"
              size="md"
            >
              Create Customer
            </Button>
            <Button onClick={handleCustomerModal} variant="secondary" size="md">
              View Customers ({customersRes?.customers?.length})
            </Button>
            <Button
              onClick={() => refetchCustomers()}
              variant="secondary"
              size="md"
            >
              refetch
            </Button>
          </div>
        </div>
      </div>

      {/* Create Order Modal */}
      <Modal
        isOpen={isCreateOrderOpen}
        onClose={handleCreateOrderModal}
        title="Create New Order"
        size="xl"
      >
        <div className="space-y-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium">Order Information</h3>
            <Button onClick={generateOrderData} variant="outline" size="sm">
              Generate Sample Data
            </Button>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Customer ID
              </label>
              <input
                type="text"
                value={orderForm.customer_id}
                onChange={(e) =>
                  handleOrderFormChange("customer_id", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter customer ID"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Customer Name
              </label>
              <input
                type="text"
                value={orderForm.customer_name}
                onChange={(e) =>
                  handleOrderFormChange("customer_name", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter customer name"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Customer Email
              </label>
              <input
                type="email"
                value={orderForm.customer_email}
                onChange={(e) =>
                  handleOrderFormChange("customer_email", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter customer email"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Customer Phone
              </label>
              <input
                type="text"
                value={orderForm.customer_phone}
                onChange={(e) =>
                  handleOrderFormChange("customer_phone", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter customer phone"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Payment Method
            </label>
            <select
              value={orderForm.payment_method}
              onChange={(e) =>
                handleOrderFormChange("payment_method", e.target.value)
              }
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="credit_card">Credit Card</option>
              <option value="debit_card">Debit Card</option>
              <option value="bank_transfer">Bank Transfer</option>
              <option value="cash">Cash</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Shipping Address
            </label>
            <div className="grid grid-cols-2 gap-2">
              <input
                type="text"
                value={orderForm.shipping_address.street}
                onChange={(e) =>
                  handleOrderFormChange("shipping_address", {
                    ...orderForm.shipping_address,
                    street: e.target.value,
                  })
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Street"
              />
              <input
                type="text"
                value={orderForm.shipping_address.city}
                onChange={(e) =>
                  handleOrderFormChange("shipping_address", {
                    ...orderForm.shipping_address,
                    city: e.target.value,
                  })
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="City"
              />
              <input
                type="text"
                value={orderForm.shipping_address.state}
                onChange={(e) =>
                  handleOrderFormChange("shipping_address", {
                    ...orderForm.shipping_address,
                    state: e.target.value,
                  })
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="State"
              />
              <input
                type="text"
                value={orderForm.shipping_address.zip_code}
                onChange={(e) =>
                  handleOrderFormChange("shipping_address", {
                    ...orderForm.shipping_address,
                    zip_code: e.target.value,
                  })
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="ZIP Code"
              />
              <input
                type="text"
                value={orderForm.shipping_address.country}
                onChange={(e) =>
                  handleOrderFormChange("shipping_address", {
                    ...orderForm.shipping_address,
                    country: e.target.value,
                  })
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Country"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Order Items
            </label>
            <Button
              onClick={addOrderItem}
              variant="outline"
              size="sm"
              className="mb-2"
            >
              Add Item
            </Button>
            {orderForm.items.map((item, index) => (
              <div key={index} className="border p-3 rounded-md mb-2">
                <div className="grid grid-cols-4 gap-2 mb-2">
                  <input
                    type="text"
                    value={item.product_name}
                    onChange={(e) =>
                      updateOrderItem(index, "product_name", e.target.value)
                    }
                    className="p-2 border border-gray-300 rounded-md"
                    placeholder="Product name"
                  />
                  <input
                    type="number"
                    value={item.quantity}
                    onChange={(e) =>
                      updateOrderItem(
                        index,
                        "quantity",
                        parseInt(e.target.value)
                      )
                    }
                    className="p-2 border border-gray-300 rounded-md"
                    placeholder="Quantity"
                  />
                  <input
                    type="number"
                    value={item.unit_price}
                    onChange={(e) =>
                      updateOrderItem(
                        index,
                        "unit_price",
                        parseFloat(e.target.value)
                      )
                    }
                    className="p-2 border border-gray-300 rounded-md"
                    placeholder="Unit price"
                  />
                  <Button
                    onClick={() => removeOrderItem(index)}
                    variant="ghost"
                    size="sm"
                  >
                    Remove
                  </Button>
                </div>
              </div>
            ))}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Notes
            </label>
            <textarea
              value={orderForm.notes}
              onChange={(e) => handleOrderFormChange("notes", e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
              rows={3}
              placeholder="Enter order notes"
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              onClick={handleCreateOrderModal}
              variant="secondary"
              size="md"
            >
              Cancel
            </Button>
            <Button
              onClick={handleCreateOrder}
              variant="primary"
              size="md"
              loading={loading}
            >
              Create Order
            </Button>
          </div>
        </div>
      </Modal>

      {/* Create Product Modal */}
      <Modal
        isOpen={isCreateProductOpen}
        onClose={handleCreateProductModal}
        title="Create New Product"
        size="lg"
      >
        <div className="space-y-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium">Product Information</h3>
            <Button onClick={generateProductData} variant="outline" size="sm">
              Generate Sample Data
            </Button>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Product Name
              </label>
              <input
                type="text"
                value={productForm.name}
                onChange={(e) =>
                  handleProductFormChange("name", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter product name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                SKU
              </label>
              <input
                type="text"
                value={productForm.sku}
                onChange={(e) => handleProductFormChange("sku", e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter SKU"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={productForm.description}
              onChange={(e) =>
                handleProductFormChange("description", e.target.value)
              }
              className="w-full p-2 border border-gray-300 rounded-md"
              rows={3}
              placeholder="Enter product description"
            />
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category
              </label>
              <input
                type="text"
                value={productForm.category}
                onChange={(e) =>
                  handleProductFormChange("category", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter category"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Brand
              </label>
              <input
                type="text"
                value={productForm.brand}
                onChange={(e) =>
                  handleProductFormChange("brand", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter brand"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Price
              </label>
              <input
                type="number"
                value={productForm.price}
                onChange={(e) =>
                  handleProductFormChange("price", parseFloat(e.target.value))
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter price"
                step="0.01"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Stock Quantity
              </label>
              <input
                type="number"
                value={productForm.stock_quantity}
                onChange={(e) =>
                  handleProductFormChange(
                    "stock_quantity",
                    parseInt(e.target.value)
                  )
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter stock quantity"
              />
            </div>
            <div className="flex items-center">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={productForm.is_active}
                  onChange={(e) =>
                    handleProductFormChange("is_active", e.target.checked)
                  }
                  className="mr-2"
                />
                <span className="text-sm font-medium text-gray-700">
                  Active
                </span>
              </label>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              onClick={handleCreateProductModal}
              variant="secondary"
              size="md"
            >
              Cancel
            </Button>
            <Button
              onClick={handleCreateProduct}
              variant="primary"
              size="md"
              loading={loading}
            >
              Create Product
            </Button>
          </div>
        </div>
      </Modal>

      {/* Create Payment Modal */}
      <Modal
        isOpen={isCreatePaymentOpen}
        onClose={handleCreatePaymentModal}
        title="Create New Payment"
        size="lg"
      >
        <div className="space-y-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium">Payment Information</h3>
            <Button onClick={generatePaymentData} variant="outline" size="sm">
              Generate Sample Data
            </Button>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Order ID
              </label>
              <input
                type="text"
                value={paymentForm.order_id}
                onChange={(e) =>
                  handlePaymentFormChange("order_id", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter order ID"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Customer ID
              </label>
              <input
                type="text"
                value={paymentForm.customer_id}
                onChange={(e) =>
                  handlePaymentFormChange("customer_id", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter customer ID"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Amount
              </label>
              <input
                type="number"
                value={paymentForm.amount}
                onChange={(e) =>
                  handlePaymentFormChange("amount", parseFloat(e.target.value))
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter amount"
                step="0.01"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Currency
              </label>
              <select
                value={paymentForm.currency}
                onChange={(e) =>
                  handlePaymentFormChange("currency", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
              >
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="GBP">GBP</option>
                <option value="JPY">JPY</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Transaction Type
              </label>
              <select
                value={paymentForm.transaction_type}
                onChange={(e) =>
                  handlePaymentFormChange("transaction_type", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
              >
                <option value="purchase">Purchase</option>
                <option value="refund">Refund</option>
                <option value="capture">Capture</option>
                <option value="void">Void</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Payment Method
              </label>
              <select
                value={paymentForm.payment_method}
                onChange={(e) =>
                  handlePaymentFormChange("payment_method", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
              >
                <option value="credit_card">Credit Card</option>
                <option value="debit_card">Debit Card</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="digital_wallet">Digital Wallet</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Payment Provider
              </label>
              <select
                value={paymentForm.payment_provider}
                onChange={(e) =>
                  handlePaymentFormChange("payment_provider", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
              >
                <option value="stripe">Stripe</option>
                <option value="paypal">PayPal</option>
                <option value="square">Square</option>
                <option value="adyen">Adyen</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              onClick={handleCreatePaymentModal}
              variant="secondary"
              size="md"
            >
              Cancel
            </Button>
            <Button
              onClick={handleCreatePayment}
              variant="primary"
              size="md"
              loading={loading}
            >
              Create Payment
            </Button>
          </div>
        </div>
      </Modal>

      {/* Create Customer Modal */}
      <Modal
        isOpen={isCreateCustomerOpen}
        onClose={handleCreateCustomerModal}
        title="Create New Customer"
        size="xl"
      >
        <div className="space-y-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium">Customer Information</h3>
            <Button onClick={generateCustomerData} variant="outline" size="sm">
              Generate Sample Data
            </Button>
          </div>

          {/* Basic Information */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                First Name *
              </label>
              <input
                type="text"
                value={customerForm.first_name}
                onChange={(e) =>
                  handleCustomerFormChange("first_name", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter first name"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Last Name *
              </label>
              <input
                type="text"
                value={customerForm.last_name}
                onChange={(e) =>
                  handleCustomerFormChange("last_name", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter last name"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email *
              </label>
              <input
                type="email"
                value={customerForm.email}
                onChange={(e) =>
                  handleCustomerFormChange("email", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter email address"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Phone
              </label>
              <input
                type="tel"
                value={customerForm.phone}
                onChange={(e) =>
                  handleCustomerFormChange("phone", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter phone number"
              />
            </div>
          </div>

          {/* Address Information */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Address Line 1
              </label>
              <input
                type="text"
                value={customerForm.address_line1}
                onChange={(e) =>
                  handleCustomerFormChange("address_line1", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter street address"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Address Line 2
              </label>
              <input
                type="text"
                value={customerForm.address_line2}
                onChange={(e) =>
                  handleCustomerFormChange("address_line2", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter apartment, suite, etc."
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                City
              </label>
              <input
                type="text"
                value={customerForm.city}
                onChange={(e) =>
                  handleCustomerFormChange("city", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter city"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                State
              </label>
              <input
                type="text"
                value={customerForm.state}
                onChange={(e) =>
                  handleCustomerFormChange("state", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter state"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Postal Code
              </label>
              <input
                type="text"
                value={customerForm.postal_code}
                onChange={(e) =>
                  handleCustomerFormChange("postal_code", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter postal code"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Country
              </label>
              <input
                type="text"
                value={customerForm.country}
                onChange={(e) =>
                  handleCustomerFormChange("country", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter country"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date of Birth
              </label>
              <input
                type="date"
                value={customerForm.date_of_birth}
                onChange={(e) =>
                  handleCustomerFormChange("date_of_birth", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Gender
              </label>
              <select
                value={customerForm.gender}
                onChange={(e) =>
                  handleCustomerFormChange("gender", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
              >
                <option value="prefer_not_to_say">Prefer not to say</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Company Name
              </label>
              <input
                type="text"
                value={customerForm.company_name}
                onChange={(e) =>
                  handleCustomerFormChange("company_name", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter company name"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tax ID
              </label>
              <input
                type="text"
                value={customerForm.tax_id}
                onChange={(e) =>
                  handleCustomerFormChange("tax_id", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter tax ID"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tags
              </label>
              <input
                type="text"
                value={customerForm.tags}
                onChange={(e) =>
                  handleCustomerFormChange("tags", e.target.value)
                }
                className="w-full p-2 border border-gray-300 rounded-md"
                placeholder="Enter tags (comma-separated)"
              />
            </div>
          </div>

          {/* Marketing Preferences */}
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="marketing_emails"
                checked={customerForm.marketing_emails}
                onChange={(e) =>
                  handleCustomerFormChange("marketing_emails", e.target.checked)
                }
                className="rounded border-gray-300"
              />
              <label
                htmlFor="marketing_emails"
                className="text-sm font-medium text-gray-700"
              >
                Marketing Emails
              </label>
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="marketing_sms"
                checked={customerForm.marketing_sms}
                onChange={(e) =>
                  handleCustomerFormChange("marketing_sms", e.target.checked)
                }
                className="rounded border-gray-300"
              />
              <label
                htmlFor="marketing_sms"
                className="text-sm font-medium text-gray-700"
              >
                Marketing SMS
              </label>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Notes
            </label>
            <textarea
              value={customerForm.notes}
              onChange={(e) =>
                handleCustomerFormChange("notes", e.target.value)
              }
              className="w-full p-2 border border-gray-300 rounded-md"
              placeholder="Enter additional notes"
              rows={3}
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              onClick={handleCreateCustomerModal}
              variant="secondary"
              size="md"
            >
              Cancel
            </Button>
            <Button
              onClick={handleCreateCustomer}
              variant="primary"
              size="md"
              loading={loading}
            >
              Create Customer
            </Button>
          </div>
        </div>
      </Modal>

      {/* View Orders Modal */}
      <Modal
        isOpen={isOrdersOpen}
        onClose={handleOrdersModal}
        title="All Orders"
        size="xl"
      >
        <div className="space-y-4">
          {isOrdersLoading ? (
            <div className="text-center py-8">Loading orders...</div>
          ) : ordersRes?.orders?.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No orders found
            </div>
          ) : (
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {ordersRes?.orders?.map((order: Order) => (
                <div key={order._id} className="border p-4 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold">Order #{order.order_id}</h4>
                    <span
                      className={`px-2 py-1 rounded-full text-xs ${
                        order.status === "delivered"
                          ? "bg-green-100 text-green-800"
                          : order.status === "cancelled"
                          ? "bg-red-100 text-red-800"
                          : "bg-yellow-100 text-yellow-800"
                      }`}
                    >
                      {order.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    {order.customer_name} - {order.customer_email}
                  </p>
                  <p className="text-sm text-gray-600 mb-2">
                    Total: ${order.total_amount}
                  </p>
                  <p className="text-xs text-gray-500">
                    {new Date(order.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </Modal>

      {/* View Products Modal */}
      <Modal
        isOpen={isProductsOpen}
        onClose={handleProductsModal}
        title="All Products"
        size="xl"
      >
        <div className="space-y-4">
          {isProductsLoading ? (
            <div className="text-center py-8">Loading products...</div>
          ) : productsRes?.products?.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No products found
            </div>
          ) : (
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {productsRes?.products?.map((product: Product) => (
                <div key={product._id} className="border p-4 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold">{product.name}</h4>
                    <span
                      className={`px-2 py-1 rounded-full text-xs ${
                        product.is_active
                          ? "bg-green-100 text-green-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      {product.is_active ? "Active" : "Inactive"}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    {product.description}
                  </p>
                  <div className="flex justify-between items-center">
                    <p className="text-sm text-gray-600">SKU: {product.sku}</p>
                    <p className="text-sm font-medium">${product.price}</p>
                  </div>
                  <p className="text-xs text-gray-500">
                    Stock: {product.stock_quantity} | Category:{" "}
                    {product.category}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </Modal>

      {/* View Payments Modal */}
      <Modal
        isOpen={isPaymentsOpen}
        onClose={handlePaymentsModal}
        title="All Payments"
        size="xl"
      >
        <div className="space-y-4">
          {isPaymentsLoading ? (
            <div className="text-center py-8">Loading payments...</div>
          ) : paymentsRes?.payments?.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No payments found
            </div>
          ) : (
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {paymentsRes?.payments?.map((payment: Payment) => (
                <div key={payment._id} className="border p-4 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold">
                      Payment #{payment.payment_id}
                    </h4>
                    <span
                      className={`px-2 py-1 rounded-full text-xs ${
                        payment.status === "completed"
                          ? "bg-green-100 text-green-800"
                          : payment.status === "failed"
                          ? "bg-red-100 text-red-800"
                          : payment.status === "pending"
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {payment.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    Order: {payment.order_id}
                  </p>
                  <p className="text-sm text-gray-600 mb-2">
                    Amount: {payment.currency} {payment.amount}
                  </p>
                  <p className="text-sm text-gray-600 mb-2">
                    Method: {payment.payment_method} via{" "}
                    {payment.payment_provider}
                  </p>
                  <p className="text-xs text-gray-500">
                    {new Date(payment.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </Modal>

      {/* View Customers Modal */}
      <Modal
        isOpen={isCustomerOpen}
        onClose={handleCustomerModal}
        title="All Customers"
        size="xl"
      >
        <div className="space-y-4">
          {isCustomersLoading ? (
            <div className="text-center py-8">Loading customers...</div>
          ) : customersRes?.customers?.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No customers found
            </div>
          ) : (
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {customersRes?.customers?.map((customer: Customer) => (
                <div key={customer.id} className="border p-4 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="font-semibold">
                        {customer.first_name} {customer.last_name}
                      </h4>
                      <p className="text-sm text-gray-600">
                        @{customer.username} | {customer.customer_id}
                      </p>
                    </div>
                    <div className="flex space-x-2">
                      <span
                        className={`px-2 py-1 rounded-full text-xs ${
                          customer.is_active
                            ? "bg-green-100 text-green-800"
                            : "bg-red-100 text-red-800"
                        }`}
                      >
                        {customer.is_active ? "Active" : "Inactive"}
                      </span>
                      <span
                        className={`px-2 py-1 rounded-full text-xs ${
                          customer.is_verified
                            ? "bg-blue-100 text-blue-800"
                            : "bg-gray-100 text-gray-800"
                        }`}
                      >
                        {customer.is_verified ? "Verified" : "Unverified"}
                      </span>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{customer.email}</p>
                  {customer.phone && (
                    <p className="text-sm text-gray-600 mb-2">
                      Phone: {customer.phone}
                    </p>
                  )}
                  {customer.address_line1 && (
                    <p className="text-sm text-gray-600 mb-2">
                      Address: {customer.address_line1}
                      {customer.city && `, ${customer.city}`}
                      {customer.state && `, ${customer.state}`}
                      {customer.country && `, ${customer.country}`}
                    </p>
                  )}
                  {customer.company_name && (
                    <p className="text-sm text-gray-600 mb-2">
                      Company: {customer.company_name}
                    </p>
                  )}
                  {customer.tags && (
                    <p className="text-xs text-gray-500 mb-2">
                      Tags: {customer.tags}
                    </p>
                  )}
                  <div className="flex justify-between items-center">
                    <div className="flex space-x-2">
                      <span
                        className={`px-2 py-1 rounded-full text-xs ${
                          customer.email_verified
                            ? "bg-green-100 text-green-800"
                            : "bg-gray-100 text-gray-800"
                        }`}
                      >
                        Email {customer.email_verified ? "✓" : "✗"}
                      </span>
                      <span
                        className={`px-2 py-1 rounded-full text-xs ${
                          customer.phone_verified
                            ? "bg-green-100 text-green-800"
                            : "bg-gray-100 text-gray-800"
                        }`}
                      >
                        Phone {customer.phone_verified ? "✓" : "✗"}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500">
                      Created:{" "}
                      {new Date(customer.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </Modal>

      {/* View Users Modal */}
      <Modal
        isOpen={isUsersOpen}
        onClose={handleUsersModal}
        title="All Users"
        size="lg"
      >
        <div className="space-y-4">
          <div className="text-center py-8 text-gray-500">
            User management functionality coming soon...
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default DataHuntPage;
