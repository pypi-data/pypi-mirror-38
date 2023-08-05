-- Torishop data class

do
	TorishopData = {}
	TorishopData.__index = TorishopData
	local cln = {}
	setmetatable(cln, TorishopData)
		
	function TorishopData:getSaleItem()
		itemData = {
			id = 0,
		 	name= nil,
			tcOld = nil,
			tc = nil,
			usdOld = nil,
			usd = nil
		}
		if (not TORISHOP_DATA) then
			local file = io.open("torishop/torishop.txt")
			if (not file) then
				return false
			end
			for ln in file:lines() do
				if string.match(ln, "^PRODUCT") then
					local segments = 19
					local data_stream = { ln:match(("([^\t]*)\t"):rep(segments)) }
					if (data_stream[6] == "1") then
						itemData.id = data_stream[4]
						itemData.name = data_stream[5]
						itemData.tcOld = tonumber(data_stream[9])
						itemData.tc = tonumber(data_stream[7])
						itemData.usdOld = tonumber(data_stream[10])
						itemData.usd = tonumber(data_stream[8])
						return itemData
					end
				end
			end
		    file:close()
		end
		return TORISHOP_DATA.sale
	end
	
end