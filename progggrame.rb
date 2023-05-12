puts "====bienvenue au xin dragon d'or===="
puts "que voulez-vous emporter? "

@menu={"nassi poulet" => ["7€"],"nassi porc" => ["7€"],"riz spécial poulet" => ["7€"],"riz spécial porc" => ["7€"]}
@menu.keys.each_with_index do |item,i|
	puts "#{i+1} - #{item}"
end
@sthelse=true
@commande=[]
choix=gets.chomp
while @sthelse do
	if choix.to_i > 0
		if choix.to_i > 4
			puts "dire un chiffre entre 1 et 4"
		elsif ["no","non","c'est tout","ce sera tout"].any? {|x|k.include?(x)}
			@sthelse=false
		else
			puts @menu.keys[(choix - 1)]
			@commande.push(choix)
			puts "autre chose?"
			k=gets.chomp
			if ["no","non","c'est tout","ce sera tout"].any? {|x|k.include?(x)}
				@sthelse=false

			end
		end
	else
		
		@sthelse=false
	end
end
if @commande.length == 0
	puts "ok, bye"
elsif @commande.length == 1
	puts "5 minutes"
else
end