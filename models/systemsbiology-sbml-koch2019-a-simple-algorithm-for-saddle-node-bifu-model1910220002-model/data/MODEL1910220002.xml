%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%           SIMPLE 1D BIFURCATION ALGORITHM v1.0        %
%                BY DANIEL KOCH, October 2019           %
%                                                       %
%      Simple algorithm that approximates a 1D          %
%      bifurcation diagram. Works for saddle-node       %
%      bifurcations only.                               %
%      For more details see                             %
%      https://insilicovitro.wordpress.com/             %
%      2019/10/08/home-baked-bifurcation-diagrams/      %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function BifurcationAlgorithm
clc
clear
close all
% model parameters 
global k1; global k2; global k3; global k4; global n1; global n2;
k1=20; k3=5; k2=20; k4=5; n1=1.95; n2=1.3;

%%%%%% SETTINGS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ODEsystem=@model1;
opts = odeset('RelTol',1e-3,'AbsTol',1e-3, 'Refine', 3); % absolute and relative tolerance of the integrator determine the speed of the algorithm
n = 25;                   % number of control parameter values of bifurcation diagram (= resolution of the diagram)
maxIterations = 30;       % maximum number of iterations for the algorithm to identify unstable steady states
parMin = 22; parMax = 26; % maximum and minimum values 
integrationTime = 600;    % choose big enough so that the system reaches steady state for all values of the control parameter 
                          % (if the time is too short, bifurcation diagrams can look distorted)

% refining the resolution in the vicinity of the saddle node bifucations
I1 = linspace(23.1,23.4,10);
I2 = linspace(24.25,24.35,10);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% some auxilliary variables
param_interval = linspace(parMin,parMax,n);
param_interval = [param_interval I1 I2];
param_interval = sort(param_interval);
data = zeros(length(param_interval),6);        % first column is the value of the control parameter, remaining columns for 
                                               % the (un-)/stable steady states of the system variables 
S1_SS1 = 0;
S1_unstable = -1;   % the value -1 functions as auxilliary index, indicating that no unstable steady exits for a given value of the control parameter
S1_SS2 = 0;
S2_SS1 = 0;
S2_unstable = -1;
S2_SS2 = 0;

linCol=jet(maxIterations);


%% numerical approximation of bifurcation data
try
for j = 1:length(param_interval)
    try
    	%close(figure(1));
    end
       for i = 0:1 
            k1 = param_interval(j);
            %% inital simulations starting with low/high S1/S2
            % simulate to steady state          
            if i == 0;
               S1 = 0; S2 = 1;
               [t1,s1] = ode23s(ODEsystem, [0,integrationTime], [S1,S2] , opts);
               S1_SS1 = s1(length(s1),1); 
               S2_SS1 = s1(length(s1),2);
            else
                S1 = 10; S2 = 1;
               [t1,s1] = ode23s(ODEsystem, [0,integrationTime], [S1,S2] , opts); 
               S1_SS2 = s1(length(s1),1);
               S2_SS2 = s1(length(s1),2);
               S1_unstable = -1;
               S2_unstable = -1;
               if abs(S1_SS2-S1_SS1) >= min(S1_SS2,S1_SS1)/100 % check if steady states are different by at least 1%
                    %% auxilliary variables
                    nextS1 = (S1_SS1+S1_SS2)/2; % next initial conditions
                    nextS2 = (S2_SS1+S2_SS2)/2;
                    currentSS1 = 0;             % steady states resulting from a 
                    currentSS2 = 0;
                    lastS1_SS1 = S1_SS1;        % temporary storage variables
                    lastS1_SS2 = S1_SS2; 
                    lastS2_SS1 = S2_SS1; 
                    lastS2_SS2 = S2_SS2; 
                    bin1 = [0; 0]; bin2 = [0; 0]; % temporary storage for time course data for S1/S2 from which unstable steady states can be approximated
                   
                   %% iterative identification/approximation of unstable steady state (this is the main part of the algorithm)
                    ii = 0;
                    while  ii < maxIterations
                        ii = ii + 1;     
                        
                        %% uncomment for monitoring of algorithm - show convergence of initial conditions of S1/S2
%                         figure(1); 
%                         subplot(2,2,1)
%                         set(gcf, 'Position', [600 100 800 600]);
%                         hold on; box on; axis square;
%                         xlabel('n','Interpreter','latex', 'fontsize',12.5); ylabel('[S1] at t$_0$','Interpreter','latex', 'fontsize',12.5);
%                         set(gca, 'TickLabelInterpreter', 'latex', 'fontsize',12);
%                         title('iterations','Interpreter','latex', 'fontsize',12.5);
%                         plot(ii,nextS1,'xk');
%                         subplot(2,2,3)
%                         hold on; box on;axis square;
%                         xlabel('n','Interpreter','latex', 'fontsize',12.5); ylabel('[S2] at t$_0$','Interpreter','latex', 'fontsize',12.5);
%                         set(gca, 'TickLabelInterpreter', 'latex', 'fontsize',12);
%                         plot(ii,nextS2,'xk');
                        
                        %% simulate to steady state
                        [t1,s1] = ode23s(ODEsystem, [0,integrationTime], [nextS1,nextS2] , opts);
                        currentSS1 = s1(length(s1),1); currentSS2 = s1(length(s1),2);  % steady state resulting from last initial conditions
                        bin1 = [bin1; s1(:,1)]; bin2 = [bin2; s1(:,2)]; % put concentration values of timecourses into temporary storage without temporal information

                        %% uncomment for monitoring of algorithm - show timecourses
%                         figure(1); 
%                         subplot(2,2,2) 
%                         axis square; box on; hold on; xlim([0 200]);
%                         xlabel('time (s)','Interpreter','latex', 'fontsize',12.5); ylabel('[S1]','Interpreter','latex', 'fontsize',12.5);
%                         set(gca, 'TickLabelInterpreter', 'latex', 'fontsize',12);
%                         title('time courses','Interpreter','latex', 'fontsize',12.5);
%                         plot(t1, s1(:,1),'-','color',linCol(ii,:),'Linewidth', 1.5);
%                         colormap(jet(maxIterations)); caxis([0 maxIterations]); c = colorbar; title(c,'iteration','Interpreter','latex', 'fontsize',11); set(c, 'TickLabelInterpreter', 'latex', 'fontsize',11);
%                         
%                         subplot(2,2,4) 
%                         axis square; box on; hold on; xlim([0 200]);
%                         xlabel('time (s)','Interpreter','latex', 'fontsize',12.5); ylabel('[S2]','Interpreter','latex', 'fontsize',12.5);
%                         set(gca, 'TickLabelInterpreter', 'latex', 'fontsize',12);
%                         title('time courses','Interpreter','latex', 'fontsize',12.5);
%                         plot(t1, s1(:,2),'-','color',linCol(ii,:),'Linewidth', 1.5); 
%                         colormap(jet(maxIterations)); caxis([0 maxIterations]); c = colorbar; title(c,'iteration','Interpreter','latex', 'fontsize',11); set(c, 'TickLabelInterpreter', 'latex', 'fontsize',11);
%                         %print(['Frame ' num2str(ii)], '-dpng', '-r150');
%                         %%create frames for animated GIF
                        
                        %% test whether potential unstable steady state collapsed into either of the stable steady states
                        if abs(S1_SS2 - currentSS1) < (S1_SS2/100) % (as the steady states of S1 and S2 are linked, performing the test for S1 is sufficient)
                            S1_unstable = -2;   % the value -2 is an auxilliary index imdicating that a unstable steady state must exist but has not been identified yet
                            S2_unstable = -2;                       
                            lastS1_SS2 = nextS1;  % update temporary storage variables
                            lastS2_SS2 = nextS2;
                            nextS1 = (nextS1+lastS1_SS1)/2;  %determine initial conditions for next iteration step
                            nextS2 = (nextS2+lastS2_SS1)/2;
                        elseif abs(S1_SS1 - currentSS1) < (S1_SS1/100) 
                            S1_unstable = -2;
                            S2_unstable = -2;
                            lastS1_SS1 = nextS1;
                            lastS2_SS1 = nextS2;
                            nextS1 = (nextS1+lastS1_SS2)/2;
                            nextS2 = (nextS2+lastS2_SS2)/2;
                        else
                            % test whether potential SS is stable +/- 1% since at least 10 integration steps
                            stable = true;
                            for iii = 1:10
                                deviation = abs(1-(s1(length(s1)-iii,1)/(currentSS1)));
                                if deviation > 0.01
                                    deviation = abs(1-(s1(length(s1)-iii,2)/(currentSS2)));
                                    if deviation > 0.01
                                         stable = false;
                                    end
                                end
                            end
                            if stable 
                                S1_unstable = currentSS1; % assigning the identified unstable steady states
                                S2_unstable = currentSS2;
                                ii = maxIterations; % make exit condition true
                            else
                                S1_unstable = -2; % the value -2 is an auxilliary index imdicating that a unstable steady state must exist but has not been identified yet
                                S2_unstable = -2;
                            end
                        end
                    end
                    
                    if S1_unstable == -2  %perform approximation of unstable steady state if iterative identification did not converge within iteration limit
                        
                        bin1 = bin1(find(abs(bin1-S1_SS1)> (S1_SS1/90)));  %remove values close to the stable steady states (within 1/90 = 1.111...% of the SS)
                        bin1 = bin1(find(abs(bin1-S1_SS2)> (S1_SS2/90)));
                        [N,E] = histcounts(bin1,250); % creates a histogram of the most abundant concentration values (excluding stable steady states) 
                                                      % from all timecourses divided into 250 containers with boundaries E and counts N
                        [V I] = max(N); % find index I of the container with highest count number
                        S1_unstable = (E(I)+E(I+1))/2;   % approximate unstable steady state as the arithmetic middle of the 
                                                    % adjacent boundaries of the container with the highest count
                        
                        bin2 = bin2(find(abs(bin2-S2_SS1)> (S2_SS1/90))); % repeat approximation for S2
                        bin2 = bin2(find(abs(bin2-S2_SS2)> (S2_SS2/90)));
                        [N,E] = histcounts(bin2,250);
                        [V I] = max(N);
                        S2_unstable = (E(I)+E(I+1))/2;
                    end
               else
               end
               data(j, 1:7) = [param_interval(j) S1_SS1 S1_unstable S1_SS2  S2_SS1 S2_unstable S2_SS2]; % store indentified/approximated steady states in data matrix
            end
       end    
end
end
% plotting bifurcation diagrams
    try
    u1 = find(data(:,3) ~= -1); %identify positions with unstable steady states
    figure(2)
    
    % bifurcation diagram for S1
    subplot(1,2,1);
    hold on;
    box on;
    axis square;
    xlim([param_interval(1) param_interval(length(param_interval))])
    xlabel('k1','Interpreter','latex', 'fontsize',12.5); 
    ylabel('[S1]','Interpreter','latex', 'fontsize',12.5);
    set(gca, 'TickLabelInterpreter', 'latex', 'fontsize',12);
    
     if size(u1)>0              % plot if bistability occurs
        SN1 = u1(1);  % position of first saddle node bifurcation
        SN2 = u1(length(u1));  % position of second saddle node bifurcation
        plot(data(1:SN2,1),data(1:SN2,2),'-b','Linewidth',2);  % plot stable region until first saddle node bifurcation
        plot([data(SN2,1) data(SN2,1)],[data(SN2,2) data(SN2,3)],':','Color',[0.4,0.4,0.4],'Linewidth',2);  % draw connection line between stable/unstable region for continuity of diagram
        plot(data(SN1:SN2,1),data(SN1:SN2,3),':','Color',[0.4,0.4,0.4],'Linewidth',2);  % plot unstable region 
        plot([data(SN1,1) data(SN1,1)],[data(SN1,3) data(SN1,4)],':','Color',[0.4,0.4,0.4],'Linewidth',2);  % draw connection line between stable/unstable region for continuity of diagram
        plot(data(SN1:size(data,1),1),data(SN1:size(data,1),4),'-b','Linewidth',2); % plot stable region from second saddle node bifurcation onwards
     else
         plot(data(1:size(data,1),1),data(1:size(data,1),2),'-b','Linewidth',2);   % plot if no bistability occurs
     end

    % bifurcation diagram for S2
    subplot(1,2,2);
    hold on;
    box on;
    axis square;
    xlim([param_interval(1) param_interval(length(param_interval))])
    xlabel('k1','Interpreter','latex', 'fontsize',12.5); 
    ylabel('[S2]','Interpreter','latex', 'fontsize',12.5);
    set(gca, 'TickLabelInterpreter', 'latex', 'fontsize',12);
    if size(u1)>0       % see comments above for description
        SN1 = u1(1);
        SN2 = u1(length(u1));
        plot(data(1:SN2,1),data(1:SN2,5),'-r','Linewidth',2);    
        plot([data(SN2,1) data(SN2,1)],[data(SN2,5) data(SN2,6)],':','Color',[0.4,0.4,0.4],'Linewidth',2); 
        plot(data(SN1:SN2,1),data(SN1:SN2,6),':','Color',[0.4,0.4,0.4],'Linewidth',2);
        plot([data(SN1,1) data(SN1,1)],[data(SN1,6) data(SN1,7)],':','Color',[0.4,0.4,0.4],'Linewidth',2); 
        plot(data(SN1:size(data,1),1),data(SN1:size(data,1),7),'-r','Linewidth',2);
    else
         plot(data(1:size(data,1),1),data(1:size(data,1),5),'-r','Linewidth',2);   
    end
    end
% dlmwrite('data.dat',data,'\t');  write data to file
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% create animated GIF from frames
% GifName = 'BifurAlgoConvergence.gif';
% delay = 0.3;    % Delay between frames (s)
% for ii = 1:23
%     [A, ~] = imread(['Frame ' num2str(ii) '.png']);
%     [X, map] = rgb2ind(A, 256);
%     if ii == 1
%         imwrite(X, map, GifName, 'gif', 'LoopCount', inf, 'DelayTime', delay)
%     else
%         imwrite(X, map, GifName, 'gif', 'WriteMode', 'append', 'DelayTime', delay)
%     end
% end

end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function dxdt = model1(t,s)

global k1; global k2; global k3; global k4; global n1; global n2;

S1 = s(1);
S2 = s(2);

%ODEs
dS1dt= k1/(1+S2^n1) - k3*S1;
dS2dt= k2/(1+S1^n2) - k4*S2;

dxdt = [dS1dt; dS2dt];
end
