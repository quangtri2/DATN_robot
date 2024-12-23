USE [QL_Nhap_Kho(DATN)]
GO
/****** Object:  Trigger [dbo].[trg_UpdateTongKho]    Script Date: 12/3/2024 7:52:17 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER TRIGGER [dbo].[trg_UpdateTongKho]
ON [dbo].[Bang_Nhap_Kho]
AFTER INSERT
AS
BEGIN
    -- Cập nhật số lượng trong bảng TongKho sau khi có bản ghi được insert vào bảng NhapKho
    UPDATE Bang_Tong_Kho
    SET SoLuong = SoLuong + i.SoLuongNhap
    FROM Bang_Tong_Kho t
    INNER JOIN inserted i ON t.MaHang = i.MaHang;

END;
