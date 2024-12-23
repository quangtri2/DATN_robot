USE [QL_Nhap_Kho(DATN)]
GO
/****** Object:  Table [dbo].[Bang_Nhap_Kho]    Script Date: 12/3/2024 7:55:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Bang_Nhap_Kho](
	[MaHang] [nvarchar](50) NULL,
	[TenHang] [nvarchar](50) NULL,
	[XuatXu] [nvarchar](50) NULL,
	[SoLuongNhap] [int] NULL,
	[ThoiGianNhap] [datetime] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[Bang_Tong_Kho]    Script Date: 12/3/2024 7:55:52 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Bang_Tong_Kho](
	[MaHang] [nchar](10) NOT NULL,
	[TenHang] [nvarchar](50) NULL,
	[XuatXu] [nvarchar](50) NULL,
	[SoLuong] [int] NULL,
 CONSTRAINT [PK_Bang_Tong_Kho] PRIMARY KEY CLUSTERED 
(
	[MaHang] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
INSERT [dbo].[Bang_Nhap_Kho] ([MaHang], [TenHang], [XuatXu], [SoLuongNhap], [ThoiGianNhap]) VALUES (N'002       ', N'Petrol ', N'Russia', 1, CAST(N'2024-12-03 19:38:05.000' AS DateTime))
INSERT [dbo].[Bang_Nhap_Kho] ([MaHang], [TenHang], [XuatXu], [SoLuongNhap], [ThoiGianNhap]) VALUES (N'002       ', N'Petrol ', N'Russia', 1, CAST(N'2024-12-03 19:51:21.000' AS DateTime))
INSERT [dbo].[Bang_Nhap_Kho] ([MaHang], [TenHang], [XuatXu], [SoLuongNhap], [ThoiGianNhap]) VALUES (N'001       ', N'Fuel oil', N'Nigeria', 1, CAST(N'2024-12-03 19:51:40.000' AS DateTime))
INSERT [dbo].[Bang_Nhap_Kho] ([MaHang], [TenHang], [XuatXu], [SoLuongNhap], [ThoiGianNhap]) VALUES (N'001       ', N'Fuel oil', N'Nigeria', 1, CAST(N'2024-12-03 19:53:41.000' AS DateTime))
INSERT [dbo].[Bang_Tong_Kho] ([MaHang], [TenHang], [XuatXu], [SoLuong]) VALUES (N'001       ', N'Fuel oil', N'Nigeria', 10)
INSERT [dbo].[Bang_Tong_Kho] ([MaHang], [TenHang], [XuatXu], [SoLuong]) VALUES (N'002       ', N'Petrol ', N'Russia', 6)
INSERT [dbo].[Bang_Tong_Kho] ([MaHang], [TenHang], [XuatXu], [SoLuong]) VALUES (N'003       ', N'Diesel fuel', N'Iran', 12)
