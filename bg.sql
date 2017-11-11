DROP DATABASE IF EXISTS bg;
CREATE DATABASE  bg;

\c bg;

-- GRANT SELECT, INSERT ON DATABASE bg TO bgtemp;

CREATE EXTENSION pgcrypto;

-- CREATE USER bgtemp with login;

DROP TABLE IF EXISTS login;
CREATE TABLE login (
  loginID SERIAL UNIQUE,
  email varchar(50) NOT NULL UNIQUE,
  fname text NOT NULL,
  lname text  NOT NULL,
  pw1 text NOT NULL,
  zipcode varchar(5) NOT NULL,
  userLevel text NOT NULL,
  PRIMARY KEY (loginID)
  );

INSERT INTO login VALUES (DEFAULT,'bkertche@umw.edu','Brendon', 'Kertcher', crypt('pass', gen_salt('bf')), '22407','Administrator');
INSERT INTO login VALUES (DEFAULT,'scripture187@gmail.com','Billy', 'Andrews', crypt('pass', gen_salt('bf')), '22407','Administrator');
INSERT INTO login VALUES (DEFAULT,'jhuffma3@umw.edu','Jacob', 'Huffman', crypt('pass', gen_salt('bf')), '22407','Administrator');
INSERT INTO login VALUES (DEFAULT,'manager@umw.edu','Test', 'test', crypt('pass', gen_salt('bf')), '22407','Manager');
INSERT INTO login VALUES (DEFAULT,'sales@umw.edu','Test', 'test', crypt('pass', gen_salt('bf')), '22407','Sales Associate');
INSERT INTO login VALUES (DEFAULT,'customer@umw.edu','Test', 'test', crypt('pass', gen_salt('bf')), '22407','Customer');
INSERT INTO login VALUES (DEFAULT,'administrator@umw.edu','Test', 'test', crypt('pass', gen_salt('bf')), '22407','Administrator');
GRANT SELECT, INSERT, DELETE, UPDATE ON login TO bgtemp;



DROP TABLE IF EXISTS items;
CREATE TABLE items (
  productID varchar NOT NULL UNIQUE,
  cost float NOT NULL,
  category text NOT NULL,
  name varchar NOT NULL,
  description varchar NOT NULL,
  PRIMARY KEY (productID)
  );

-- use two " '' " to use an apostrophe, like 'McCoy''s BBQ'
INSERT INTO items (productID, cost, category, name, description) VALUES (485, 3.99, 'Battery', 'Battery Cleaner - Acid Detector', 'BG Battery Cleaner – Acid Detector removes corrosion from battery terminals, cables and carriers. It also turns red to warn of the presence of acid or a crack or leak around terminal.');
INSERT INTO items (productID, cost, category, name, description) VALUES (985, 3.99, 'Battery', 'Battery Terminal Protectors', 'BG Battery Terminal Protectors protect battery terminals from corrosive buildup. The chemical formula is harmless to the battery, paint and other parts.  Fits easily onto the battery posts.');
INSERT INTO items (productID, cost, category, name, description) VALUES (490, 3.99, 'Battery', 'Ignition & Battery Terminal Sealer', 'BG Ignition & Battery Terminal Sealer completely seals and weatherproofs wiring and electrical connections.');
INSERT INTO items (productID, cost, category, name, description) VALUES (885, 3.99, 'Battery', 'Battery Cleaner & Leak Detector', 'BG Battery Cleaner & Leak Detector removes corrosion from battery terminals, cables and carriers. It also turn reds to warn of the presence of acid or a crack or leak around terminal.');
INSERT INTO items (productID, cost, category, name, description) VALUES (979, 3.99, 'Battery', 'Battery Cable Savers', 'BG Battery Cable Savers correct this problem by filling in the extra space, allowing the cable to be tightened to complete a solid connection. A solid connection eliminates the starting problems that the faulty connection causes.');
INSERT INTO items (productID, cost, category, name, description) VALUES (841, 3.99, 'Brakes', 'Low Viscosity DOT 4 Brake Fluid', 'BG Low Viscosity DOT 4 Brake Fluid delivers quick brake response at low temperatures for all DOT 4 disc and drum brake systems. ');
INSERT INTO items (productID, cost, category, name, description) VALUES (840, 3.99, 'Brakes', 'DOT 4 Brake Fluid', 'BG DOT 4 Brake Fluid provides the ultimate high temperature protection and moisture resistance for all DOT 4 disc and drum brake systems. Brake systems can produce pressure up to 2000 psi. This pressure, along with extreme heat from the friction of braking, cause brake fluid to break down. This compromised brake fluid will boil at a lower temperature leaving air pockets and condensation in the brake system. Water in the brake system causes a myriad of problems such as brake deposits and varnish buildup.');
INSERT INTO items (productID, cost, category, name, description) VALUES (835, 3.99, 'Brakes', 'Super DOT 4 Brake Fluid', 'BG Super DOT 4 Brake Fluid provides the ultimate high temperature protection and high boiling point protection above and beyond regular DOT 4 fluid. Brake systems can produce pressure up to 2000 psi! This pressure – along with extreme heat from the friction of braking – causes brake fluid to break down. This compromised brake fluid will boil at a lower temperature leaving air pockets and condensation in the brake system. Water in the brake system causes a myriad of problems such as brake deposits and varnish buildup.');
INSERT INTO items (productID, cost, category, name, description) VALUES (850, 3.99, 'Brakes', 'DOT 3 Brake Fluid', 'BG DOT 3 Brake Fluid provides the ultimate high temperature protection and moisture resistance for all DOT 3 disc and drum brake systems. Brake systems can produce pressure up to 2000 psi. This pressure, along with extreme heat from the friction of braking, cause brake fluid to break down. This compromised brake fluid will boil at a lower temperature leaving air pockets and condensation in the brake system. Water in the brake system causes a myriad of problems such as brake deposits and varnish buildup.');
INSERT INTO items (productID, cost, category, name, description) VALUES ('FES400', 3.99, 'Brakes', 'Xpress Brake System Fluid Exchange System', 'BG Xpress Brake System Fluid Exchange System is a small machine that quickly and effectively removes oxidized and corrosive brake fluid, replacing it with new fluid. The exchange is performed in minutes. Brakes work by creating friction to slow and stop a vehicle. This friction creates a substantial amount of heat which in turn causes rapid oxidation of brake fluid. Deposits form in the brake system causing serious brake system malfunction which compromises the vehicle’s safety.');
INSERT INTO items (productID, cost, category, name, description) VALUES ('PF7', 3.99, 'Brakes', 'PF7 Brake Service System', 'Brake Service System quickly and effectively removes oxidized and corrosive brake fluid, replacing it with new fluid. The exchange is performed in minutes in a contained unit. No hassle. No mess.');
INSERT INTO items (productID, cost, category, name, description) VALUES (402, 3.99, 'Brakes', '402 Brake & Contact Cleaner', 'BG 402 Brake & Contact Cleaner is a quick and efficient brake cleaner that dissolves built up residue on brake components. Residue on brake components leads to obnoxious brake squeal and chatter. Brake systems are sensitive to the buildup of brake fluid, grease, oil, moisture, and other residue that can form on drum and disc assemblies. ');
INSERT INTO items (productID, cost, category, name, description) VALUES (403, 3.99, 'Brakes', '403 Non-Chlorinated Brake Cleaner', 'Like BG 402, BG 403 Non-Chlorinated Brake Cleaner is a quick and efficient brake cleaner that dissolves built up residue on brake components, but without chlorinated solvents.');
INSERT INTO items (productID, cost, category, name, description) VALUES (860, 3.99, 'Brakes', 'Stop Squeal', 'BG Stop Squeal eliminates annoying, whining, or squealing brakes.');
INSERT INTO items (productID, cost, category, name, description) VALUES ('605BK', 3.99, 'Brakes', 'Brake Lube', 'BG Brake Lube is a professional-use brake grease. BG Brake Lube is applied to the caliper bracket that holds the brake pad in place. This allows pads to slide and contact the brake rotor as they wear down. Without BG Brake Lube on these caliper brackets, the brake pad may not slide inward correctly, which can cause brake pads to wear unevenly. BG Brake Lube performs exceptionally well in all applications and under all conditions. It mixes with virtually any soap-based grease with excellent seal compatibility.');
INSERT INTO items (productID, cost, category, name, description) VALUES (709, 3.99, 'Climate', 'Frigi-Clean', 'BG Frigi-Clean removes accumulated bacteria, mold, spores, road grime, nicotine oil, and debris and restores heating/cooling efficiency.');
INSERT INTO items (productID, cost, category, name, description) VALUES (702, 3.99, 'Climate', 'Universal Frigi-Quiet for R-1234yf', 'BG Universal Frigi-Quiet for R-1234yf enhances cooling, ensures quieter compressor operation and prolongs compressor life.');
INSERT INTO items (productID, cost, category, name, description) VALUES (701, 3.99, 'Climate', 'Universal Frigi-Quiet for R-134a', 'BG Universal Frigi-Quiet for R-134a enhances cooling, ensures quieter compressor operation and prolongs compressor life.');
INSERT INTO items (productID, cost, category, name, description) VALUES (704, 3.99, 'Climate', 'Universal Frigi-Charge', 'BG Universal Frigi-Charge extends compressor life and provides overall quieter and cooler running A/C systems.');
INSERT INTO items (productID, cost, category, name, description) VALUES (708, 3.99, 'Climate', 'Frigi-Fresh', 'BG Frigi-Fresh will safely and effectively eliminate foul, musty odors from A/C systems.');
INSERT INTO items (productID, cost, category, name, description) VALUES (917-2, 3.99, 'Climate', 'Mechanical Additive Injector Tool', 'The BG Mechanical Additive Injector Tool is the perfect choice for manually adding BG Universal Frigi-Quiet to a charged air conditioning system. This quick and easy, professional-use tool is designed for use without charging stations or manifold gauge sets.');
INSERT INTO items (productID, cost, category, name, description) VALUES (546, 3.99, 'Cooling', 'Universal Super Cool', 'BG Universal Super Cool protects against foaming and corrosion and restores critical coolant additive balance and coolant pH.');
INSERT INTO items (productID, cost, category, name, description) VALUES (540, 3.99, 'Cooling', 'Universal Cooling System Cleaner', 'BG Universal Cooling System Cleaner removes built-up scale, oil, and harsh mineral deposits. It also removes tough residues caused by oil fouling and coolant inhibitor breakdown.');
INSERT INTO items (productID, cost, category, name, description) VALUES (511, 3.99, 'Cooling', 'Universal Cooling System Sealer', 'BG Universal Cooling System Sealer quickly and completely plugs leak points in the coolant system. Refined organic fibers carry sealer particles that build on each other around a hole until it is completely plugged.');
INSERT INTO items (productID, cost, category, name, description) VALUES ('FES200', 3.99, 'Cooling', 'Xpress Cooling System Fluid Exchange System', 'BG Xpress Cooling System Fluid Exchange System is a small machine that quickly and efficiently installs new coolant while simultaneously removing worn out coolant.');
INSERT INTO items (productID, cost, category, name, description) VALUES ('CT2', 3.99, 'Cooling', 'CT2 Coolant Transfusion System', 'BG CT2 Coolant Transfusion System quickly and efficiently installs new 50/50 coolant while simultaneously removing worn out coolant.');
INSERT INTO items (productID, cost, category, name, description) VALUES (589, 3.99, 'Cooling', 'Universal Coolant/Antifreeze', 'BG Universal Coolant/Antifreeze offers complete and long-lasting cooling system protection under the most severe conditions. It is designed to be used in all gasoline, diesel, and compressed natural gas fueled engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES ('CT4', 3.99, 'Cooling', 'CT4 Coolant Transfusion System', 'BG CT4 Coolant Transfusion System uses a vacuum to remove worn out coolant from the cooling system and then installs new 50/50 coolant back into the system with no air pockets.');
INSERT INTO items (productID, cost, category, name, description) VALUES ('CT6', 3.99, 'Cooling', 'CT6 Large Capacity Coolant Transfusion System', 'BG CT6 Large Capacity Coolant Transfusion System vacuums out used coolant and then installs new coolant.');
INSERT INTO items (productID, cost, category, name, description) VALUES (587, 3.99, 'Cooling', 'AB Complete', 'BG AB Complete rejuvenates worn out coolant, giving it back its corrosion prevention abilities.');
INSERT INTO items (productID, cost, category, name, description) VALUES (245, 3.99, 'Diesel', '245 Premium Diesel Fuel System Cleaner', 'BG 245 Premium Diesel Fuel System Cleaner removes and dissolves deposits from the entire diesel injection system, including fuel injectors and combustion chambers.');
INSERT INTO items (productID, cost, category, name, description) VALUES (244, 3.99, 'Diesel', '244', 'BG 244 is a powerhouse diesel fuel system cleaner. BG 244 is like BG 44K for diesels.');
INSERT INTO items (productID, cost, category, name, description) VALUES (229, 3.99, 'Diesel', 'Diesel Care', 'BG Diesel Care is a highly effective diesel fuel injection system cleaner.');
INSERT INTO items (productID, cost, category, name, description) VALUES (9700-550, 3.99, 'Diesel', 'Diesel VIA', 'BG Diesel VIA is the ultimate diesel injector cleaning system for passenger cars, SUVs and light trucks.');
INSERT INTO items (productID, cost, category, name, description) VALUES (227, 3.99, 'Diesel', 'DFC with Lubricity', 'BG DFC with Lubricity is a superior multi-functional diesel fuel conditioner.');
INSERT INTO items (productID, cost, category, name, description) VALUES (230, 3.99, 'Diesel', 'DFC Plus', 'BG DFC Plus is a professional-use diesel conditioner that guards fuel system components against corrosion, corrects nozzle buildup, and keeps the fuel system clean.');
INSERT INTO items (productID, cost, category, name, description) VALUES (247, 3.99, 'Diesel', 'DFC Plus Easy Treat', 'BG DFC Plus Easy Treat contains all the benefits of BG DFC Plus concentrated in a conveniently-sized bottle for individual truck tanks.');
INSERT INTO items (productID, cost, category, name, description) VALUES (248, 3.99, 'Diesel', 'DFC Plus with Cetane Improver', 'BG DFC Plus with Cetane Improver protects fuel system components from corrosion and deposits, prevents fuel gelling, and reduces exhaust smoke. It is a professional use diesel conditioner containing a lubricity agent that protects against the effects of low-sulfur diesel and a cetane improver that raises the diesel cetane rating by 3-7 values.');
INSERT INTO items (productID, cost, category, name, description) VALUES (225, 3.99, 'Diesel', 'DFC with Lubricity HP', 'BG DFC with Lubricity HP is a diesel fuel conditioner plus lubricity for high pressure common rail diesels.');
INSERT INTO items (productID, cost, category, name, description) VALUES (232, 3.99, 'Diesel', 'DFC Plus HP', 'BG DFC Plus HP for high pressure common rail diesel engines provides excellent fuel system protection for the high temperatures and pressures of high pressure diesel systems.');
INSERT INTO items (productID, cost, category, name, description) VALUES (237, 3.99, 'Diesel', 'DFC Plus HP Extra Cold Weather Performance', 'BG DFC Plus HP Extra Cold Weather Performance cleans fuel injector deposits and prevents black fuel filter plugging in High Pressure Common Rail (HPCR) systems.');
INSERT INTO items (productID, cost, category, name, description) VALUES (240, 3.99, 'Diesel', 'DFC Plus for Biodiesel', 'BG DFC Plus for Biodiesel conditions biodiesel, cleans fuel systems, and helps to prevent fuel deposits. It’s safe for both common rail and direct injection fuel engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES (256, 3.99, 'Diesel', 'Diesel Thaw', 'BG Diesel Thaw quickly and efficiently liquefies gelled diesel fuel and melts ice crystals, restoring fuel flow.');
INSERT INTO items (productID, cost, category, name, description) VALUES (255, 3.99, 'Diesel', 'Diesel ISC Induction System Cleaner', 'BG Diesel ISC Induction System Cleaner powers through oil deposits and unburned fuel left behind by exhaust system.');
INSERT INTO items (productID, cost, category, name, description) VALUES (9255-550, 3.99, 'Diesel', 'Diesel Induction Service Set', 'As part of the Diesel Induction Service, the BG Diesel Induction Service Set sends BG Diesel ISC Induction System Cleaner through the EGR runners and the fresh air intake.');
INSERT INTO items (productID, cost, category, name, description) VALUES (2581, 3.99, 'Diesel', 'DPF & Emissions System Restoration', 'BG DPF & Emissions System Restoration safely dissolves and removes hydrocarbon deposits, especially soot, from the air intake and emissions system. Used by a professional with the BG 12Q VIA, PN 9300, this product restores fuel economy, reduces emissions and prolongs component life. ');
INSERT INTO items (productID, cost, category, name, description) VALUES (9300, 3.99, 'Diesel', '12Q VIA', 'BG 12Q VIA, PN 9300, is a one-of-a-kind diesel intake and emissions system cleaning machine that allows technicians to not only command Diesel Particulate Filter (DPF) regeneration, but to control it for a thorough cleaning. ');
INSERT INTO items (productID, cost, category, name, description) VALUES (233, 3.99, 'Diesel', 'Diesel Fuel De-icer', 'BG Diesel Fuel De-icer is specially formulated to protect wet, high cloud point diesel fuel from icing.');
INSERT INTO items (productID, cost, category, name, description) VALUES (215, 3.99, 'Diesel', 'Diesel Fuel Pour Depressant', 'BG Diesel Fuel Pour Depressant improves fuel pumpability in cold weather conditions without altering other diesel fuel properties.');
INSERT INTO items (productID, cost, category, name, description) VALUES (228, 3.99, 'Diesel', 'Diesel Fuel Cetane Improver', 'BG Diesel Cetane Improver increases the cetane number of diesel fuel. For a diesel fuel conditioner with added cetane improver, check out BG DFC Plus with Cetane Improver.');
INSERT INTO items (productID, cost, category, name, description) VALUES (224, 3.99, 'Diesel', 'Diesel Pump Lubricant', 'BG Diesel Pump Lubricant provides the needed lubricity to that prevents low-sulfur diesel fuels from scuffing and scoring on the surfaces of fuel injection pump.');
INSERT INTO items (productID, cost, category, name, description) VALUES (751, 3.99, 'DriveLine', 'Ultra-Guard LS Full Synthetic Gear Lubricant', 'BG Ultra-Guard LS Full Synthetic Gear Lubricant provides the ultimate in simplicity and ease when servicing for drive line components, especially those requiring limited slip function.');
INSERT INTO items (productID, cost, category, name, description) VALUES (753, 3.99, 'DriveLine', 'Ultra-Guard LS Heavy Duty', 'BG Ultra-Guard LS Heavy Duty provides the ultimate in simplicity and ease when servicing for drive line components, especially those requiring limited slip function.');
INSERT INTO items (productID, cost, category, name, description) VALUES (792, 3.99, 'DriveLine', 'Syncro Shift II', 'BG Syncro ShiftII is a specially formulated gear lubricant designed for front wheel drive manual transmissions. It reduces maintenance costs by improving thermal stability, low-temperature fluidity, and shear stability while providing smoother shifting and improved seal compatibility.');
INSERT INTO items (productID, cost, category, name, description) VALUES (939, 3.99, 'DriveLine', 'Drive Line Service Center', 'The BG Drive Line Service Center provides a fast, easy, and clean way of servicing all types of automotive differentials, manual transmissions, manual transaxles and transfer cases in light- and heavy-duty vehicles.');
INSERT INTO items (productID, cost, category, name, description) VALUES (752, 3.99, 'DriveLine', 'Ultra Guard Heavy Duty', 'BG Ultra-Guard Heavy Duty provides the ultimate protection for drive line components. Specifically designed for heavy duty and commercial vehicles, it has superior thermal stability, smoother gear shifting, optimum drive line efficiency, quieter operation, protection against wear, pitting, and corrosion, seal compatibility and improved seal performance.');
INSERT INTO items (productID, cost, category, name, description) VALUES (750, 3.99, 'DriveLine', 'Ultra-Guard Full Synthetic Gear Lubricant', 'BG Ultra-Guard is a revolutionary multi-purpose synthetic gear oil compatible with all car and truck applications calling for GL-5 gear oil. It provides superior thermal stability, smoother gear shifting, optimum drive line efficiency, quieter operation, protection against wear, pitting, and corrosion, seal compatibility and improved seal performance.');
INSERT INTO items (productID, cost, category, name, description) VALUES (328, 3.99, 'DriveLine', 'Universal MGC', 'BG Universal MGC is designed to protect both conventional and limited slip differentials. It enhances lubricant film thickness and improves extreme pressure characteristics of any gear oil.');
INSERT INTO items (productID, cost, category, name, description) VALUES (325, 3.99, 'DriveLine', 'MGC Multi-Gear Concentrate', 'BG MGC is an innovative professional-use gear oil additive that enhances film thickness and strength, improves thermal stability and lubricant life, and smooths manual transmission shifting characteristics. It will reduce component wear, gear box temperature, and limited slip differential chatter.');
INSERT INTO items (productID, cost, category, name, description) VALUES (110, 3.99, 'Engine', 'MOA', 'BG MOA is the number one engine oil supplement! In a recent survey, dealership service managers chose BG MOA 8 to 1 over the next aftermarket supplier.');
INSERT INTO items (productID, cost, category, name, description) VALUES (115, 3.99, 'Engine', 'Extended Life MOA', 'BG Extended Life MOA is formulated with 100 percent synthetic chemistry to protect engine components and fortify all brands of engine oil over extended oil change intervals.');
INSERT INTO items (productID, cost, category, name, description) VALUES (109, 3.99, 'Engine', 'EPR Engine Performance Restoration', 'BG EPR Engine Performance Restoration is a powerhouse of an engine cleaner! It effectively softens, emulsifies and dissolves even the most stubborn fuel gums that clog rings.');
INSERT INTO items (productID, cost, category, name, description) VALUES (729, 3.99, 'Engine', 'SAE 0W-20 Full Synthetic Engine Oil', 'BG SAE 0W-20 Full Synthetic Engine Oil is a high quality oil designed for gasoline passenger cars, vans, and light trucks requiring API SN and preceding engine oil.');
INSERT INTO items (productID, cost, category, name, description) VALUES (737, 3.99, 'Engine', 'SAE 5W-30 Full Synthetic Engine Oil', 'BG SAE 5W-30 Full Synthetic Engine Oil is formulated to give superb performance for gasoline and diesel engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES (730, 3.99, 'Engine', 'Hi-L0W30 Full Synthetic Engine Oil', 'BG Hi-L0W30 is a revolutionary full synthetic engine oil; it flows immediately to lubricate vital engine components.');
INSERT INTO items (productID, cost, category, name, description) VALUES (775, 3.99, 'Engine', 'SAE 10W-30 Synthetic Blend Engine Oil', 'BG SAE 10W-30 Synthetic Blend Engine Oil offers outstanding wear protection and oil evaporation prevention. As a professional-use product, it lubricates and cools internal engine surfaces, flows at temperatures as low as -40°F (-40°C), and resists thickening.');
INSERT INTO items (productID, cost, category, name, description) VALUES (112, 3.99, 'Engine', 'DOC Diesel Oil Conditioner', 'BG DOC Diesel Oil Conditioner is designed to condition oil in high-output diesel engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES (777, 3.99, 'Engine', 'High-Performance 4-Stroke Engine Oil', 'BG High-Performance 4-Stroke Engine Oil is a revolutionary synthetic blend engine oil formulated to provide maximum small engine protection.');
INSERT INTO items (productID, cost, category, name, description) VALUES (773, 3.99, 'Engine', 'Synthetic 2-Stroke Engine Oil for Air-Cooled Engines', 'BG Synthetic 2-Stroke Engine Oil for Air-Cooled Engines is a blend of performance oils and proprietary additives specifically for small, air-cooled engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES (772, 3.99, 'Engine', 'Synthetic 2-Stroke Engine Oil for Water-Cooled Engines', 'BG Synthetic 2-Stroke Engine Oil for Water-Cooled Engines is a blend of performance oils and proprietary additives specifically for small, water-cooled engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES (714, 3.99, 'Engine', 'SAE 15W-40 Synthetic Blend Engine Oil', 'BG SAE 15W-40 Synthetic Blend Engine Oil offers outstanding wear and evaporation protection for engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES (713, 3.99, 'Engine', 'SAE 10W-30 HD Synthetic Blend Engine Oil', 'BG SAE 10W-30 HD Synthetic Blend Engine Oil offers outstanding wear and evaporation protection for engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES (107, 3.99, 'Engine', 'BG RF-7 Oil Treatment', 'BG RF-7 is an oil treatment specially formulated to increase engine compression and power by increasing oil viscosity. It contains additives that keep oil from thickening, protect vital engine parts from corrosive damage, and help seal rings to increase compression and reduce blow-by.');
INSERT INTO items (productID, cost, category, name, description) VALUES (716, 3.99, 'Engine', 'Shear Power HD', 'BG Shear Power HD is an extended life, premium oil for diesel engines requiring API CK-4 or gasoline engines requiring API SN and preceding engine oil.');
INSERT INTO items (productID, cost, category, name, description) VALUES (105, 3.99, 'Engine', 'Quick Clean for Engines', 'BG Quick Clean for Engines safely and effectively removes  deposits from engine components.');
INSERT INTO items (productID, cost, category, name, description) VALUES (116, 3.99, 'Engine', 'Engine Performance Concentrate', 'BG Engine Performance Concentrate provides critical protection for small engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES (120, 3.99, 'Engine', 'Engine Purge', 'BG Engine Purge is a fix-it product designed to safely remove accumulated sludge and other deposits from the engine.');
INSERT INTO items (productID, cost, category, name, description) VALUES (208, 3.99, 'Gasoline', '44K Fuel System Cleaner', 'BG 44K is the number one fuel injector cleaner! In a recent survey, dealership service managers chose BG 44K® 6 to 1 over the next aftermarket supplier.');
INSERT INTO items (productID, cost, category, name, description) VALUES (201, 3.99, 'Gasoline', 'Fuel Injection & Combustion Chamber Cleaner', 'BG Fuel Injection & Combustion Chamber Cleaner is an especially effective gasoline direct injection system cleanup product.');
INSERT INTO items (productID, cost, category, name, description) VALUES (210, 3.99, 'Gasoline', 'Fuel Injection System Cleaner', 'BG Fuel Injection System Cleaner removes rock-hard carbon deposits from fuel injectors, intake valves and ports.');
INSERT INTO items (productID, cost, category, name, description) VALUES (260, 3.99, 'Gasoline', 'GDI Intake Valve Cleaner', 'BG GDI Intake Valve Cleaner is a BG lab-tested and proof-positive intake cleaner for all engines (both port fuel injection and gasoline direct injection).');
INSERT INTO items (productID, cost, category, name, description) VALUES (206, 3.99, 'Gasoline', 'Air Intake System Cleaner', 'BG Air Intake System Cleaner removes deposits that can accumulate in the air throttle body assemblies and plenums.');
INSERT INTO items (productID, cost, category, name, description) VALUES (9290-200, 3.99, 'Gasoline', 'VIA Vehicle Injection Apparatus', 'As part of the BG Fuel/Air Induction Service, the BG VIA Vehicle Injection Apparatus provides a highly effective cleaning of the entire fuel system. The BG VIA is a supply tool pressurized by shop air. ');
INSERT INTO items (productID, cost, category, name, description) VALUES (9209, 3.99, 'Gasoline', 'Air Intake System Cleaning Tool', 'The BG Air Intake System Cleaning Tool, PN 9209, is specially designed for use with BG GDI Intake Valve Cleaner‚ PN 260‚ to remove sticky, heavy deposits inside the air throttle body and plenum area.');
INSERT INTO items (productID, cost, category, name, description) VALUES (213, 3.99, 'Gasoline', 'Ethanol Fuel System Defender', 'BG Ethanol System Defender protects the fuel system from the harmful effects of ethanol. It keeps intake manifolds, intake ports, intake valves, and combustion chambers free of deposits caused by ethanol.');
INSERT INTO items (productID, cost, category, name, description) VALUES (212, 3.99, 'Gasoline', 'Ethanol Corrosion Preventer', 'BG Ethanol Corrosion Preventer forms a protective coating on fuel system components to defend against corrosion. It contains special stabilizers that keep the entire fuel system clean, restoring power and fuel efficiency.');
INSERT INTO items (productID, cost, category, name, description) VALUES (281, 3.99, 'Gasoline', 'Ethanol Fuel System Drier', 'BG Ethanol Fuel System Drier defends engines against the water that accumulates in ethanol-blended fuel.');
INSERT INTO items (productID, cost, category, name, description) VALUES (202, 3.99, 'Gasoline', 'Supercharge II', 'BG Supercharge II keeps the fuel system clean and free of fuel deposits. With special stabilizers that prevent fuel oxidation, and gum and varnish formation, it prevents rust and corrosion and provides long-term fuel storage stability.');
INSERT INTO items (productID, cost, category, name, description) VALUES (203, 3.99, 'Gasoline', 'CF5', 'BG CF5 fuel system cleaner prevents deposits throughout the entire fuel system. Added at each oil change, it will keep injectors, pistons, fuel intake components and sensors clean and free of damaging deposits and corrosion.');
INSERT INTO items (productID, cost, category, name, description) VALUES (4073, 3.99, 'Gasoline', 'Mass Air Flow Sensor Cleaner', 'BG Mass Air Flow Sensor Cleaner restores Mass Air Flow Sensor and Idle Air Controller function. It quickly cleans all materials contained in these components including hot wires, plastic, and rubber.');
INSERT INTO items (productID, cost, category, name, description) VALUES (211, 3.99, 'Gasoline', 'ISC Induction System Cleaner', 'BG ISC Induction System Cleaner quickly and safely cleans fuel injectors and removes hard, baked-on carbon deposits from intake valves, combustion chambers and EGR ports.');
INSERT INTO items (productID, cost, category, name, description) VALUES (9240, 3.99, 'Gasoline', 'EGR Service Tool', 'Used with BG ISC Induction System Cleaner, PN 211, the BG EGR Service Tool allows for total decarbonization of the fuel system.');
INSERT INTO items (productID, cost, category, name, description) VALUES (280, 3.99, 'Gasoline', 'Fuel System Drier', 'BG Fuel System Drier absorbs moisture that accumulates from condensation in the fuel tank, holding it suspension until it gets burned with fuel. Because of this, it provides easier cold weather starting and prevents fuel icing and freezing.');
INSERT INTO items (productID, cost, category, name, description) VALUES (271, 3.99, 'Gasoline', 'Gasoline Direct Injection Cleaner Part 1', 'BG Gasoline Direct Injection Cleaner is a two-part cleaning process formulated to soften and disperse baked-on deposits that accumulate on intake valves of direct injected engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES (272, 3.99, 'Gasoline', 'Gasoline Direct Injection Cleaner Part 2', 'BG Gasoline Direct Injection Cleaner is a two-part cleaning process formulated to soften and disperse baked-on deposits that accumulate on intake valves of direct injected engines.');
INSERT INTO items (productID, cost, category, name, description) VALUES (408, 3.99, 'Gasoline', 'Inject-A-Flush Injector Cleaner', 'BG Inject-A-Flush Injector Cleaner will safely and effectively clean the fuel injection system without the need to remove the injectors. Built up gums and oxidized fuel residues are dissolved in minutes and removed from the system.');
INSERT INTO items (productID, cost, category, name, description) VALUES (406, 3.99, 'Gasoline', 'Throttle Body & Intake Cleaner', 'BG Throttle Body & Intake Cleaner quickly and safely removes accumulated deposits from the butterfly/throttle valve, throttle body and idle air control valves of the air induction system.');
INSERT INTO items (productID, cost, category, name, description) VALUES (411, 3.99, 'Gasoline', 'Carb and Choke Cleaner', 'BG Carb and Choke Cleaner contains a special blend of solvents that powers through harmful carbon, gum, and varnish deposits, cleans carburetors, automatic chokes, PCV valves and lines, and manifold heat control valves.');
INSERT INTO items (productID, cost, category, name, description) VALUES (412, 3.99, 'Gasoline', 'Hi-Delivery Carb and Choke Cleaner', 'BG Hi-Delivery Carb and Choke Cleaner contain a special blend of solvents that powers through harmful carbon, gum, and varnish deposits, cleans carburetors, automatic chokes, PCV valves and lines, and manifold heat control valves.');
INSERT INTO items (productID, cost, category, name, description) VALUES (209, 3.99, 'Gasoline', '209 Fuel Induction System Cleaner', 'BG 209 Fuel Induction System Cleaner quickly and safely powers through stubborn fuel deposits that build up on fuel injectors, intake valves, ports, and combustion chambers.');

GRANT SELECT, INSERT ON items TO bgtemp;


DROP TABLE IF EXISTS warehouses;
CREATE TABLE warehouses (
  warehouseID SERIAL UNIQUE,
  warehouseName varchar NOT NULL,
  address varchar NOT NULL,
  city varchar NOT NULL,
  state varchar NOT NULL,
  zip int NOT NULL,
  email varchar(50) NOT NULL UNIQUE,
  warehouseLevel int NOT NULL,
  PRIMARY KEY (warehouseID),
  FOREIGN KEY (email) REFERENCES login (email)
  );
  
INSERT INTO warehouses VALUES (DEFAULT,'BG Main Warehouse','740 S Wichita Street','Wichita','KS',67213,'scripture187@gmail.com',1);
INSERT INTO warehouses VALUES (DEFAULT,'BG of UMW','1701 College Ave','Fredericksburg','VA',22401,'bkertche@umw.edu',2);
INSERT INTO warehouses VALUES (DEFAULT,'Mobile: Jacob','8008 Elm Street','Chicago','IL',43243,'jhuffma3@umw.edu',3);
INSERT INTO warehouses VALUES (DEFAULT,'BG of Central Virginia','116 Sylvia Road','Ashland','VA',23005,'sales@umw.edu',2);

GRANT SELECT, INSERT, DELETE ON warehouses TO bgtemp;

DROP TABLE IF EXISTS invoices;
CREATE TABLE invoices (
  invoiceID SERIAL UNIQUE,
  emailSales VARCHAR(50) NOT NULL,
  emailCust VARCHAR(50) NOT NULL,
  dateCreate DATE NOT NULL,
  dateDue DATE NOT NULL,
  amountDue FLOAT NOT NULL,
  PRIMARY KEY (invoiceID),
  FOREIGN KEY (emailSales) REFERENCES warehouses(email),
  FOREIGN KEY (emailCust) REFERENCES login(email)
  );

GRANT SELECT, INSERT ON invoices TO bgtemp;


INSERT INTO invoices VALUES (DEFAULT,'jhuffma3@umw.edu','customer@umw.edu','2017-11-05','2017-12-05',40.5);
INSERT INTO invoices VALUES (DEFAULT,'bkertche@umw.edu','jhuffma3@umw.edu','2017-11-03','2017-12-03',20.4);

DROP TABLE IF EXISTS invoiceItems;
CREATE TABLE invoiceItems (
  invoiceID int NOT NULL,
  itemID VARCHAR NOT NULL,
  quantity INT NOT NULL,
  total FLOAT NOT NULL,
  FOREIGN KEY (itemID) REFERENCES items(productID),
  FOREIGN KEY (invoiceID) REFERENCES invoices(invoiceID)
  );
  
INSERT INTO invoiceItems VALUES (1,281,8,32.0);
INSERT INTO invoiceItems VALUES (1,206,4,84.50);
INSERT INTO invoiceItems VALUES (1,213,2,30.24);
INSERT INTO invoiceItems VALUES (2,281,8,32.0);
INSERT INTO invoiceItems VALUES (2,206,4,84.50);
INSERT INTO invoiceItems VALUES (2,213,2,30.24);

GRANT SELECT, INSERT ON invoiceItems TO bgtemp;

